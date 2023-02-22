from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass

import estimagic as em
import numpy as np
from HARK.ConsumptionSaving.ConsIndShockModel import (
    ConsIndShockSolver,
    IndShockConsumerType,
)
from HARK.ConsumptionSaving.ConsPortfolioModel import init_portfolio
from HARK.ConsumptionSaving.ConsRiskyAssetModel import RiskyAssetConsumerType
from HARK.core import MetricObject, make_one_period_oo_solver
from HARK.distribution import DiscreteDistribution, DiscreteDistributionLabeled
from HARK.interpolation import (
    LinearFast,
    LinearInterpOnInterp1D,
    MargValueFuncCRRA,
    ValueFuncCRRA,
)
from HARK.interpolation._sklearn import GeneralizedRegressionUnstructuredInterp
from HARK.rewards import UtilityFuncCRRA, UtilityFunction
from HARK.utilities import NullFunc, construct_assets_grid
from scipy.optimize import Bounds, LinearConstraint, minimize


@dataclass
class PostDecisionStage(MetricObject):
    v_func: ValueFuncCRRA = NullFunc()
    dvda_func: MargValueFuncCRRA = NullFunc()
    dvdb_func: MargValueFuncCRRA = NullFunc()


@dataclass
class ConsumptionStage(MetricObject):
    c_func: LinearFast = NullFunc()
    v_func: ValueFuncCRRA = NullFunc()
    dvdl_func: MargValueFuncCRRA = NullFunc()
    dvdb_func: MargValueFuncCRRA = NullFunc()


@dataclass
class DepositStage(MetricObject):
    d_func: LinearFast = NullFunc()
    v_func: ValueFuncCRRA = NullFunc()
    dvdm_func: MargValueFuncCRRA = NullFunc()
    dvdn_func: MargValueFuncCRRA = NullFunc()


@dataclass
class PensionContribSolution(MetricObject):
    post_decision_stage: PostDecisionStage = PostDecisionStage()
    deposit_stage: DepositStage = DepositStage()
    consumption_stage: ConsumptionStage = ConsumptionStage()


GridParameters = namedtuple(
    "GridParameters",
    "aXtraMin, aXtraMax, aXtraCount, aXtraNestFac, aXtraExtra",
    defaults=[[]],
)


class PensionContribConsumerType(RiskyAssetConsumerType):
    time_inv_ = deepcopy(RiskyAssetConsumerType.time_inv_)
    time_inv_ = time_inv_ + [
        "DisutilLabor",
        "IncUnempRet",
        "TasteShkStd",
        "TaxDeduct",
    ]

    def __init__(self, **kwds):
        params = init_pension_contrib.copy()
        params.update(kwds)

        # Initialize a basic AgentType
        RiskyAssetConsumerType.__init__(self, **params)

        # Add consumer-type specific objects, copying to create independent versions
        self.solve_one_period = make_one_period_oo_solver(PensionContribSolver)

        self.update()  # Make assets grid, income process, terminal solution

    def update(self):
        self.update_grids()
        RiskyAssetConsumerType.update(self)
        self.update_distributions()

    def update_solution_terminal(self):
        # consume everything in terminal period
        c_func = lambda mNrm, nNrm: mNrm + nNrm
        # deposit nothing in terminal period
        d_func = lambda mNrm, nNrm: 0.0

        u = UtilityFuncCRRA(self.CRRA)
        v_func = lambda mNrm, nNrm: u(c_func(mNrm, nNrm))
        vp_func = lambda mNrm, nNrm: u.der(c_func(mNrm, nNrm))

        consumption_stage = ConsumptionStage(
            c_func=c_func, v_func=v_func, dvdl_func=vp_func, dvdb_func=vp_func
        )

        deposit_stage = DepositStage(
            d_func=d_func, v_func=v_func, dvdm_func=vp_func, dvdn_func=vp_func
        )

        self.solution_terminal = PensionContribSolution(
            deposit_stage=deposit_stage,
            consumption_stage=consumption_stage,
        )

    def update_grids(self):
        # retirement

        # worker grids
        self.mGrid = construct_assets_grid(
            GridParameters(self.epsilon, self.mMax, self.mCount, self.mNestFac)
        )

        self.nGrid = construct_assets_grid(
            GridParameters(0.0, self.nMax, self.nCount, self.nNestFac)
        )
        self.mMat, self.nMat = np.meshgrid(self.mGrid, self.nGrid, indexing="ij")

        # pure consumption grids
        self.aGrid = construct_assets_grid(
            GridParameters(0.0, self.aMax, self.aCount, self.aNestFac)
        )
        self.bGrid = construct_assets_grid(
            GridParameters(0.0, self.bMax, self.bCount, self.bNestFac)
        )
        self.aMat, self.bMat = np.meshgrid(self.aGrid, self.bGrid, indexing="ij")

        # pension deposit grids
        self.lGrid = construct_assets_grid(
            GridParameters(self.epsilon, self.lMax, self.lCount, self.lNestFac)
        )
        self.b2Grid = construct_assets_grid(
            GridParameters(0.0, self.b2Max, self.b2Count, self.b2NestFac)
        )
        self.lMat, self.b2Mat = np.meshgrid(self.lGrid, self.b2Grid, indexing="ij")

        self.add_to_time_inv(
            "mGrid",
            "nGrid",
            "mMat",
            "nMat",
            "aGrid",
            "bGrid",
            "aMat",
            "bMat",
            "lGrid",
            "b2Grid",
            "lMat",
            "b2Mat",
        )

    def update_distributions(self):
        # update income process
        ShockDstn = []

        for i in range(len(self.ShockDstn.dstns)):
            shock = self.ShockDstn[i]
            labeled_dstn = DiscreteDistributionLabeled(
                shock.pmv,
                shock.atoms,
                name="Joint Distribution of shocks to income and risky asset",
                var_names=["perm", "tran", "risky"],
            )

            ShockDstn.append(labeled_dstn)

        self.ShockDstn = ShockDstn


@dataclass
class PensionContribSolver(MetricObject):
    solution_next: PensionContribSolution
    DiscFac: float
    CRRA: float
    DisutilLabor: float
    Rfree: float
    TaxDeduct: float
    TranShkDstn: DiscreteDistribution
    IncUnempRet: DiscreteDistribution
    TasteShkStd: DiscreteDistribution
    ShockDstn: DiscreteDistributionLabeled
    mGrid: np.array
    nGrid: np.array
    mMat: np.ndarray
    nMat: np.ndarray
    aGrid: np.array
    bGrid: np.array
    aMat: np.ndarray
    bMat: np.ndarray
    lGrid: np.array
    b2Grid: np.array
    lMat: np.ndarray
    b2Mat: np.array

    def __post_init__(self):
        self.def_utility_funcs()

    def def_utility_funcs(self):
        self.u = UtilityFuncCRRA(self.CRRA)

        # pension deposit function: tax deduction from pension deposits
        # which is gradually decreasing in the level of deposits

        g = lambda x: self.TaxDeduct * np.log(1 + x)
        gp = lambda x: self.TaxDeduct / (1 + x)
        gp_inv = lambda x: self.TaxDeduct / x - 1

        self.g = UtilityFunction(g, gp, gp_inv)

    def solve_post_decision(self, deposit_stage_next):
        # unpack next period's solution
        dvdm_func_next = deposit_stage_next.dvdm_func
        dvdn_func_next = deposit_stage_next.dvdn_func
        v_func_next = deposit_stage_next.v_func

        def value_and_marginal_funcs(shock, aBal, bBal):
            variables = {}

            psi = shock["perm"]
            mNrm_next = aBal * self.Rfree / psi + shock["tran"]
            nNrm_next = bBal * shock["risky"] / psi

            variables["dvda"] = (
                self.DiscFac
                * self.Rfree
                * psi ** (-self.CRRA)
                * dvdm_func_next(mNrm_next, nNrm_next)
            )
            variables["dvdb"] = (
                self.DiscFac
                * psi ** (-self.CRRA)
                * shock["risky"]
                * dvdn_func_next(mNrm_next, nNrm_next)
            )
            variables["v"] = (
                self.DiscFac
                * psi ** (1 - self.CRRA)
                * v_func_next(mNrm_next, nNrm_next)
            )

            return variables

        # First calculate marginal value functions
        def dvda_func(shock, aBal, bBal):
            psi = shock["perm"]
            mNrm_next = aBal * self.Rfree / psi + shock["tran"]
            nNrm_next = bBal * shock["risky"] / psi
            return psi ** (-self.CRRA) * dvdm_func_next(mNrm_next, nNrm_next)

        dvda_end_of_prd = (
            self.DiscFac
            * self.Rfree
            * self.ShockDstn.expected(dvda_func, self.aMat, self.bMat)
        )

        dvda_end_of_prd_nvrs = self.u.derinv(dvda_end_of_prd)
        dvda_end_of_prd_nvrs_func = LinearFast(
            dvda_end_of_prd_nvrs, [self.aGrid, self.bGrid]
        )
        dvda_end_of_prd_func = MargValueFuncCRRA(dvda_end_of_prd_nvrs_func, self.CRRA)

        def dvdb_func(shock, aBal, bBal):
            psi = shock["perm"]
            mNrm_next = aBal * self.Rfree / psi + shock["tran"]
            nNrm_next = bBal * shock["risky"] / psi
            return (
                psi ** (-self.CRRA)
                * shock["risky"]
                * dvdn_func_next(mNrm_next, nNrm_next)
            )

        dvdb_end_of_prd = self.DiscFac * self.ShockDstn.expected(
            dvdb_func, self.aMat, self.bMat
        )

        dvdb_end_of_prd_nvrs = self.u.derinv(dvdb_end_of_prd)
        dvdb_end_of_prd_nvrs_func = LinearFast(
            dvdb_end_of_prd_nvrs, [self.aGrid, self.bGrid]
        )
        dvdb_end_of_prd_func = MargValueFuncCRRA(dvdb_end_of_prd_nvrs_func, self.CRRA)

        # also calculate end of period value function

        def v_func(shock, aBal, bBal):
            psi = shock["perm"]
            mNrm_next = aBal * self.Rfree / psi + shock["tran"]
            nNrm_next = bBal * shock["risky"] / psi
            return psi ** (1 - self.CRRA) * v_func_next(mNrm_next, nNrm_next)

        v_end_of_prd = self.DiscFac * self.ShockDstn.expected(
            v_func, self.aMat, self.bMat
        )

        # value transformed through inverse utility
        v_end_of_prd_nvrs = self.u.inv(v_end_of_prd)
        v_end_of_prd_nvrs_func = LinearFast(v_end_of_prd_nvrs, [self.aGrid, self.bGrid])
        v_end_of_prd_func = ValueFuncCRRA(v_end_of_prd_nvrs_func, self.CRRA)

        post_decision_stage = PostDecisionStage(
            v_func=v_end_of_prd_func,
            dvda_func=dvda_end_of_prd_func,
            dvdb_func=dvdb_end_of_prd_func,
        )
        post_decision_stage.dvda_nvrs = dvda_end_of_prd_nvrs
        post_decision_stage.dvdb_nvrs = dvdb_end_of_prd_nvrs
        post_decision_stage.vals = v_end_of_prd

        return post_decision_stage

    def solve_consumption_decision(self, post_decision_stage):
        dvda_end_of_prd_nvrs = post_decision_stage.dvda_nvrs
        dvdb_end_of_prd_nvrs = post_decision_stage.dvdb_nvrs
        v_end_of_prd = post_decision_stage.vals

        cMat = dvda_end_of_prd_nvrs  # endogenous grid method
        lMat = cMat + self.aMat

        # at l = 0, c = 0 so we need to add this limit
        lMat_temp = np.insert(lMat, 0, 0.0, axis=0)
        cMat_temp = np.insert(cMat, 0, 0.0, axis=0)

        # bMat is a regular grid, lMat is not so we'll need to use LinearInterpOnInterp1D
        c_innr_func_by_bBal = []
        for bi in range(self.bGrid.size):
            c_innr_func_by_bBal.append(LinearFast(cMat_temp[:, bi], [lMat_temp[:, bi]]))

        c_innr_func = LinearInterpOnInterp1D(c_innr_func_by_bBal, self.bGrid)
        dvdl_innr_func = MargValueFuncCRRA(c_innr_func, self.CRRA)

        # again, at l = 0, c = 0 and a = 0, so repeat dvdb[0]
        # dvdb_end_of_prd_nvrs_temp = np.insert(dvdb_end_of_prd_nvrs, 0, 0.0, axis=0)
        dvdb_end_of_prd_nvrs_temp = np.insert(
            dvdb_end_of_prd_nvrs, 0, dvdb_end_of_prd_nvrs[0], axis=0
        )

        dvdb_innr_nvrs_func_by_bBal = []
        for bi in range(self.bGrid.size):
            dvdb_innr_nvrs_func_by_bBal.append(
                LinearFast(dvdb_end_of_prd_nvrs_temp[:, bi], [lMat_temp[:, bi]])
            )

        dvdb_innr_func = MargValueFuncCRRA(
            LinearInterpOnInterp1D(dvdb_innr_nvrs_func_by_bBal, self.bGrid), self.CRRA
        )

        # make value function
        v_innr = self.u(cMat) - self.DisutilLabor + v_end_of_prd
        v_innr_nvrs = self.u.inv(v_innr)
        v_now_nvrs_temp = np.insert(v_innr_nvrs, 0, 0.0, axis=0)

        # bMat is regular grid so we can use LinearInterpOnInterp1D
        v_innr_nvrs_func_by_bBal = []
        for bi in range(self.bGrid.size):
            v_innr_nvrs_func_by_bBal.append(
                LinearFast(v_now_nvrs_temp[:, bi], [lMat_temp[:, bi]])
            )

        v_innr_nvrs_func = LinearInterpOnInterp1D(v_innr_nvrs_func_by_bBal, self.bGrid)
        v_innr_func = ValueFuncCRRA(v_innr_nvrs_func, self.CRRA)

        consumption_stage = ConsumptionStage(
            c_func=c_innr_func,
            v_func=v_innr_func,
            dvdl_func=dvdl_innr_func,
            dvdb_func=dvdb_innr_func,
        )

        return consumption_stage

    def solve_deposit_decision(self, consumption_stage):
        dvdl_func_next = consumption_stage.dvdl_func
        dvdb_func_next = consumption_stage.dvdb_func
        c_func_next = consumption_stage.c_func
        v_func_next = consumption_stage.v_func

        dvdl_innr = dvdl_func_next(self.lMat, self.b2Mat)
        dvdb_innr = dvdb_func_next(self.lMat, self.b2Mat)

        # endogenous grid method, again
        dMat = self.g.inv(dvdl_innr / dvdb_innr - 1.0)

        mMat = self.lMat + dMat
        nMat = self.b2Mat - dMat - self.g(dMat)

        consumption_stage.grids_before_cleanup = {
            "dMat": dMat,
            "mMat": mMat,
            "nMat": nMat,
            "lMat": self.lMat,
            "b2Mat": self.b2Mat,
        }

        gaussian_interp = GeneralizedRegressionUnstructuredInterp(
            dMat,
            [mMat, nMat],
            model="gaussian-process",
            std=True,
            model_kwargs={"normalize_y": True},
        )

        # evaluate d on common grid
        dMat = gaussian_interp(self.mMat, self.nMat)
        dMat = np.maximum(0.0, dMat)
        lMat = self.mMat - dMat
        b2Mat = self.nMat + dMat + self.g(dMat)

        # evaluate c on common grid
        cMat = c_func_next(lMat, b2Mat)
        # there is no consumption or deposit when there is no cash on hand
        mGrid_temp = np.append(0.0, self.mGrid)
        dMat_temp = np.insert(dMat, 0, 0.0, axis=0)
        cMat_temp = np.insert(cMat, 0, 0.0, axis=0)

        d_outr_func = LinearFast(dMat_temp, [mGrid_temp, self.nGrid])
        c_outr_func = LinearFast(cMat_temp, [mGrid_temp, self.nGrid])
        dvdm_outr_func = MargValueFuncCRRA(c_outr_func, self.CRRA)

        dvdb_innr = dvdb_func_next(lMat, b2Mat)

        dvdn_outr_nvrs = self.u.derinv(dvdb_innr)
        dvdn_outr_nvrs_temp = np.insert(dvdn_outr_nvrs, 0, dvdn_outr_nvrs[0], axis=0)
        dvdn_outr_nvrs_func = LinearFast(dvdn_outr_nvrs_temp, [mGrid_temp, self.nGrid])
        dvdn_outr_func = MargValueFuncCRRA(dvdn_outr_nvrs_func, self.CRRA)

        # make value function
        v_outr = v_func_next(lMat, b2Mat)
        v_outr_nvrs = self.u.inv(v_outr)
        # insert value of 0 at m = 0
        v_outr_nvrs_temp = np.insert(v_outr_nvrs, 0, 0.0, axis=0)
        # mMatand nMatare irregular grids so we need Curvilinear2DInterp
        v_now_nvrs_func = LinearFast(v_outr_nvrs_temp, [mGrid_temp, self.nGrid])
        v_outr_func = ValueFuncCRRA(v_now_nvrs_func, self.CRRA)

        deposit_stage = DepositStage(
            d_func=d_outr_func,
            v_func=v_outr_func,
            dvdm_func=dvdm_outr_func,
            dvdn_func=dvdn_outr_func,
        )

        deposit_stage.c_func = c_outr_func
        deposit_stage.gaussian_interp = gaussian_interp
        # deposit_stage.curvilinear_interp = curvilinear_interp

        return deposit_stage

    def solve_deposit_decision_vfi(self, consumption_stage):
        v_func_next = consumption_stage.v_func

        def objective(d_nrm, m_nrm=None, n_nrm=None):
            l_nrm = m_nrm - d_nrm
            b_nrm = n_nrm + d_nrm + self.g(d_nrm)

            v_func = v_func_next(l_nrm, b_nrm)

            output = {}

            output["contributions"] = v_func
            output["value"] = np.sum(v_func)

            return output

        res = em.maximize(
            objective,
            params=self.mMat / 2,
            criterion_kwargs={"m_nrm": self.mMat, "n_nrm": self.nMat},
            algorithm="scipy_lbfgsb",
            numdiff_options={"n_cores": 6},
            multistart=True,
            lower_bounds=np.zeros_like(self.mMat),
            upper_bounds=self.mMat,
        )

        dMat = res.params

        # for mi in range(self.mGrid.size):
        #     for ni in range(self.nGrid.size):
        #         m_nrm = self.mGrid[mi]
        #         n_nrm = self.nGrid[ni]
        #         res = minimize_scalar(
        #             objective,
        #             args=(
        #                 m_nrm,
        #                 n_nrm,
        #             ),
        #             bounds=(0, m_nrm),
        #             method="bounded",
        #         )
        #         dMat[mi, ni] = res.x

        # add d = 0 when no liquid cash
        dMat_temp = np.insert(dMat, 0, 0.0, axis=0)

        d_func = LinearFast(dMat_temp, [np.append(0.0, self.mGrid), self.nGrid])

        deposit_stage = DepositStage(
            d_func=d_func,
        )
        deposit_stage.extras = {
            "d_nrm": dMat,
            "m_nrm": self.mMat,
            "n_nrm": self.nMat,
            "res": res,
        }

        return deposit_stage

    def solve_deposit_decision_with_jac(self, consumption_stage):
        dvdl_func_next = consumption_stage.dvdl_func
        dvdb_func_next = consumption_stage.dvdb_func
        v_func_next = consumption_stage.v_func

        def objective(d_nrm, m_nrm, n_nrm):
            l_nrm = m_nrm - d_nrm
            b_nrm = n_nrm + d_nrm + self.g(d_nrm)

            return -v_func_next(l_nrm, b_nrm)

        def jacobian(d_nrm, m_nrm, n_nrm):
            l_nrm = m_nrm - d_nrm
            b_nrm = n_nrm + d_nrm + self.g(d_nrm)

            dvdl = dvdl_func_next(l_nrm, b_nrm)
            dvdb = dvdb_func_next(l_nrm, b_nrm)

            return -dvdl + dvdb * (1 + self.g.der(d_nrm))

        dMat = np.empty_like(self.mMat)

        for mi in range(self.mGrid.size):
            for ni in range(self.nGrid.size):
                m_nrm = self.mGrid[mi]
                n_nrm = self.nGrid[ni]
                res = minimize(
                    objective,
                    jac=jacobian,
                    x0=m_nrm / 2,
                    args=(
                        m_nrm,
                        n_nrm,
                    ),
                    bounds=[(0, m_nrm)],
                )
                dMat[mi, ni] = res.x

        # add d = 0 when no liquid cash
        dMat_temp = np.insert(dMat, 0, 0.0, axis=0)

        d_func = LinearFast(dMat_temp, [np.append(0.0, self.mGrid), self.nGrid])

        deposit_stage = DepositStage(
            d_func=d_func,
        )

        return deposit_stage

    def solve_vfi(self):
        deposit_solution_next = self.solution_next.deposit_stage
        post_decision_solution = self.solve_post_decision(deposit_solution_next)

        def objective(control, m_nrm, n_nrm):
            c_nrm = control[0]
            d_nrm = control[1]
            a_nrm = m_nrm - c_nrm - d_nrm
            b_nrm = n_nrm + d_nrm + self.g(d_nrm)
            value = self.u(c_nrm) + post_decision_solution.v_func(a_nrm, b_nrm)
            return -value

        cMat = np.empty_like(self.mMat)
        dMat = np.empty_like(self.mMat)
        for mi in range(self.mGrid.size):
            for ni in range(self.nGrid.size):
                m_nrm = self.mGrid[mi]
                n_nrm = self.nGrid[mi]

                bounds = Bounds([0, m_nrm], [0, m_nrm])
                linear_constraint = LinearConstraint([1, 1], [0], [m_nrm])

                sol = minimize(
                    objective,
                    x0=np.array([m_nrm / 2, m_nrm / 2]),
                    args=(
                        m_nrm,
                        n_nrm,
                    ),
                    method="trust-constr",
                    constraints=[linear_constraint],
                    bounds=bounds,
                )

                cMat[mi, ni] = sol.x[0]
                dMat[mi, ni] = sol.x[1]

    def solve(self):
        if hasattr(self.solution_next, "deposit_stage"):
            deposit_solution_next = self.solution_next.deposit_stage
        else:
            deposit_solution_next = self.solution_next

        post_decision_solution = self.solve_post_decision(deposit_solution_next)
        consumption_solution = self.solve_consumption_decision(post_decision_solution)
        deposit_solution = self.solve_deposit_decision(consumption_solution)

        solution = PensionContribSolution(
            post_decision_stage=post_decision_solution,
            consumption_stage=consumption_solution,
            deposit_stage=deposit_solution,
        )

        # solution.extras = self.solve_deposit_decision_vfi(consumption_solution)

        return solution


init_pension_contrib = init_portfolio.copy()
init_pension_contrib["Rfree"] = 1.02
init_pension_contrib["RiskyAvg"] = 1.04
init_pension_contrib["RiskyStd"] = 0.2
init_pension_contrib["RiskyCount"] = 7
init_pension_contrib["DiscFac"] = 0.98
init_pension_contrib["CRRA"] = 2.0
init_pension_contrib["DisutilLabor"] = 0.25
init_pension_contrib["TaxDeduct"] = 0.10
init_pension_contrib["LivPrb"] = [1.0]
init_pension_contrib["PermGroFac"] = [1.0]
init_pension_contrib["TranShkStd"] = [0.10]
init_pension_contrib["TranShkCount"] = 7
init_pension_contrib["PermShkStd"] = [0.10]
init_pension_contrib["PermShkCount"] = 1
init_pension_contrib["UnempPrb"] = 0.0  # Prob of unemployment while working
init_pension_contrib["IncUnemp"] = 0.0
# Prob of unemployment while retired
init_pension_contrib["UnempPrbRet"] = 0.0
init_pension_contrib["IncUnempRet"] = 0.50
init_pension_contrib["TasteShkStd"] = 0.10

init_pension_contrib["epsilon"] = 1e-6


init_pension_contrib["mCount"] = 100
init_pension_contrib["mMax"] = 50
init_pension_contrib["mNestFac"] = 2

init_pension_contrib["nCount"] = 100
init_pension_contrib["nMax"] = 50
init_pension_contrib["nNestFac"] = 2

init_pension_contrib["lCount"] = 100
init_pension_contrib["lMax"] = 50
init_pension_contrib["lNestFac"] = 2

init_pension_contrib["b2Count"] = 100
init_pension_contrib["b2Max"] = 50
init_pension_contrib["b2NestFac"] = 2

init_pension_contrib["aCount"] = 100
init_pension_contrib["aMax"] = 50
init_pension_contrib["aNestFac"] = 2

init_pension_contrib["bCount"] = 100
init_pension_contrib["bMax"] = 50
init_pension_contrib["bNestFac"] = 2


class PensionRetirementConsumerType(PensionContribConsumerType):
    def __init__(self, verbose=False, quiet=False, **kwds):
        params = init_pension_retirement.copy()
        params.update(kwds)

        # Initialize a basic AgentType
        PensionContribConsumerType.__init__(
            self, verbose=verbose, quiet=quiet, **params
        )

        # Add consumer-type specific objects, copying to create independent versions
        contrib_solver = make_one_period_oo_solver(PensionContribSolver)
        retirement_solver = make_one_period_oo_solver(ConsIndShockSolver)

        solvers = []

        for t in range(self.T_cycle):
            if t < self.T_retire:
                solvers.append(contrib_solver)
            else:
                solvers.append(retirement_solver)

        self.solve_one_period = solvers
        self.add_to_time_vary("solve_one_period")

        self.update()  # Make assets grid, income process, terminal solution

    def update_solution_terminal(self):
        return IndShockConsumerType.update_solution_terminal(self)


init_pension_retirement = init_pension_contrib.copy()
T_cycle = 15
T_retire = 10
retire_length = T_cycle - T_retire
init_pension_retirement["T_retire"] = 10
init_pension_retirement["T_cycle"] = 15
init_pension_retirement["UnempPrb"] = init_portfolio["UnempPrb"]
init_pension_retirement["IncUnemp"] = init_portfolio["IncUnemp"]
init_pension_retirement["UnempPrbRet"] = init_portfolio["UnempPrbRet"]
init_pension_retirement["IncUnempRet"] = init_portfolio["IncUnempRet"]
init_pension_retirement["LivPrb"] = init_portfolio["LivPrb"] * T_cycle
init_pension_retirement["PermGroFac"] = init_portfolio["PermGroFac"] * T_cycle
init_pension_retirement["PermShkStd"] = [0.0] * T_cycle
init_pension_retirement["TranShkStd"] = [0.01] * T_retire + [0.0] * retire_length
init_pension_retirement["PermShkCount"] = 1
init_pension_retirement["TranShkCount"] = 7
