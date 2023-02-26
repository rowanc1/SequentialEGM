from copy import copy
from dataclasses import dataclass

import numpy as np
from HARK import MetricObject
from HARK.ConsumptionSaving.ConsIndShockModel import utility, utilityP, utilityP_inv
from HARK.ConsumptionSaving.ConsLaborModel import (
    ConsumerLaborSolution,
    LaborIntMargConsumerType,
    init_labor_intensive,
)
from HARK.ConsumptionSaving.ConsPortfolioModel import (
    PortfolioConsumerType,
    init_portfolio,
)
from HARK.core import make_one_period_oo_solver
from HARK.distribution import DiscreteDistribution, calc_expectation
from HARK.interpolation import (
    BilinearInterp,
    ConstantFunction,
    LinearInterp,
    LinearInterpOnInterp1D,
    MargValueFuncCRRA,
    ValueFuncCRRA,
)
from HARK.rewards import UtilityFuncCRRA, UtilityFunction
from HARK.utilities import NullFunc


@dataclass
class PostDecisionStage(MetricObject):
    """
    This class contains the value and marginal value functions of the problem given
    post-decision states a : savings and s : risky share of portfolio.
    """

    v_func: ValueFuncCRRA = NullFunc()  # value function
    dvda_func: MargValueFuncCRRA = NullFunc()  # marginal value function wrt assets
    dvds_func: BilinearInterp = NullFunc()  # marginal value function wrt risky share
    dvda: np.array = np.array([])  # marginal value wrt a on grid
    dvds: np.array = np.array([])  # marginal value wrt s on grid


@dataclass
class PortfolioStage(MetricObject):
    """
    This class contains the policy function share : risky share of portfolio given
    decision-state a : savings, and additionally provides the value and marginal
    value functions given decision-state a.
    """

    share_func: LinearInterp = NullFunc()  # policy this stage is risky share
    v_func: ValueFuncCRRA = NullFunc()
    vp_func: MargValueFuncCRRA = NullFunc()
    vp_vals: np.array = np.array([])
    vp_nvrs: np.array = np.array([])
    aNrmMin: float = 0.0


@dataclass
class ConsumptionStage(MetricObject):
    """
    This class contains the policy function c : consumption given decision-state
    m : cash on hand. Also provides value and marginal value of m given optimal c.
    """

    c_func: LinearInterp = NullFunc()  # policy this stage is consumption
    v_func: ValueFuncCRRA = NullFunc()
    vp_func: MargValueFuncCRRA = NullFunc()
    mNrmMin: float = 0.0


@dataclass
class LaborStage(MetricObject):
    """
    This class contains the policy function of the labor decision and the value and
    marginal value functions of the state b : bank balances and theta : wages.
    """

    labor_func: LinearInterp = NullFunc()  # policy this stage is leisure/labor
    v_func: ValueFuncCRRA = NullFunc()
    vp_func: MargValueFuncCRRA = NullFunc()
    bNrmMin: float = 0.0


@dataclass
class ConsLaborPortfolioSolution(MetricObject):
    """
    The ConsLaborPortfolioSolution contains all of the solution stages of this model.
    """

    post_decision_stage: PostDecisionStage = PostDecisionStage()
    portfolio_stage: PortfolioStage = PortfolioStage()
    consumption_stage: ConsumptionStage = ConsumptionStage()
    labor_stage: LaborStage = LaborStage()

    def labor_func(self, b_nrm, t_shk):
        return self.labor_stage.labor_func(b_nrm, t_shk)

    def m_func(self, b_nrm, t_shk):
        labor = self.labor_func(b_nrm, t_shk)
        return b_nrm + labor * t_shk

    def c_func(self, b_nrm, t_shk):
        m_nrm = self.m_func(b_nrm, t_shk)
        return self.consumption_stage.c_func(m_nrm)

    def a_func(self, b_nrm, t_shk):
        m_nrm = self.m_func(b_nrm, t_shk)
        c_nrm = self.c_func(b_nrm, t_shk)
        return m_nrm - c_nrm

    def share_func(self, b_nrm, t_shk):
        a_nrm = self.a_func(b_nrm, t_shk)
        return self.portfolio_stage.share_func(a_nrm)


class LaborPortfolioConsumerType(PortfolioConsumerType, LaborIntMargConsumerType):
    time_inv_ = copy(LaborIntMargConsumerType.time_inv_)
    time_inv_ += ["DisutlLabr", "LabrCnst", "LabrShare", "LesrCnst", "LesrShare"]

    def __init__(self, verbose=False, quiet=False, **kwds):
        params = init_labor_portfolio.copy()
        params.update(kwds)

        PortfolioConsumerType.__init__(self, verbose=verbose, quiet=quiet, **params)

        self.solve_one_period = make_one_period_oo_solver(ConsLaborPortfolioSolver)

    def update(self):
        LaborIntMargConsumerType.update(self)
        PortfolioConsumerType.update(self)

    def update_LbrCost(self):
        pass

    def update_solution_terminal(self):
        # in the terminal period the risky share is trivially 0 since there is
        # no continuation; agents consume all resources and save nothing
        portfolio_stage = PortfolioStage(share_func=ConstantFunction(0.0))

        m_nrm = np.append(0.0, self.aXtraGrid)
        c_nrm = m_nrm
        c_func_terminal = LinearInterp(m_nrm, c_nrm)
        v_func_terminal = ValueFuncCRRA(c_func_terminal, self.CRRA)
        vp_func_terminal = MargValueFuncCRRA(c_func_terminal, self.CRRA)

        # in terminal period agents consume everything
        consumption_stage = ConsumptionStage(
            c_func=c_func_terminal, v_func=v_func_terminal, vp_func=vp_func_terminal
        )

        tShkGrid = self.TranShkGrid[-1]

        m_nrm_mat, t_shk_mat = np.meshgrid(m_nrm, tShkGrid, indexing="ij")

        u_prime = vp_func_terminal(m_nrm_mat)
        leisure = (u_prime * t_shk_mat / self.LesrCnst) ** (-1 / self.LesrShare)
        leisure = np.clip(leisure, 0, 1)
        labor = 1 - leisure
        b_nrm = m_nrm_mat - t_shk_mat * labor

        u_prime_inv = u_prime ** (-1 / self.CRRA)

        labor_by_tShk = []
        vPNvrsfunc_by_tShk = []
        for i in range(tShkGrid.size):
            labor_by_tShk.append(LinearInterp(b_nrm[:, i], labor[:, i]))
            vPNvrsfunc_by_tShk.append(LinearInterp(b_nrm[:, i], u_prime_inv[:, i]))

        labor_func = LinearInterpOnInterp1D(labor_by_tShk, tShkGrid)
        vPNvrsfunc_labor = LinearInterpOnInterp1D(vPNvrsfunc_by_tShk, tShkGrid)
        vp_func_labor = MargValueFuncCRRA(vPNvrsfunc_labor, self.CRRA)

        # in terminal period agents do not work, and so b = m
        # and marginal value is the same as in consumption stage
        labor_stage = LaborStage(labor_func=labor_func, vp_func=vp_func_labor)

        # create terminal solution object
        self.solution_terminal = ConsLaborPortfolioSolution(
            portfolio_stage=portfolio_stage,
            consumption_stage=consumption_stage,
            labor_stage=labor_stage,
        )


@dataclass
class ConsLaborPortfolioSolver(MetricObject):
    solution_next: ConsLaborPortfolioSolution
    TranShkDstn: DiscreteDistribution
    ShockDstn: DiscreteDistribution
    LivPrb: float
    DiscFac: float
    CRRA: float
    DisutlLabr: bool
    LabrCnst: float
    LabrShare: float
    LesrCnst: float
    LesrShare: float
    Rfree: float
    PermGroFac: float
    BoroCnstArt: float
    aXtraGrid: np.array
    ShareGrid: np.array
    TranShkGrid: np.array
    v_funcBool: float
    CubicBool: float

    def __post_init__(self):
        self.def_utility_funcs()

    def def_utility_funcs(self):
        """
        Define temporary functions for utility and its derivative and inverse
        """

        self.u = UtilityFuncCRRA(self.CRRA)

        if self.DisutlLabr:
            # use these functions if model defined by disutility of labor
            n = lambda x: -self.LabrCnst * utility(1 - x, -self.LabrShare)
            np = lambda x: self.LabrCnst * utilityP(1 - x, -self.LabrShare)
            npinv = lambda x: 1 - utilityP_inv(x / self.LabrCnst, -self.LabrShare)
        else:
            # use these functions if model defined by utility of leisure (default)
            n = lambda x: self.LesrCnst * utility(x, self.LesrShare)
            np = lambda x: self.LesrCnst * utilityP(x, self.LesrShare)
            npinv = lambda x: utilityP_inv(x / self.LesrCnst, self.LesrShare)

        self.n = UtilityFunction(n, np, npinv)

    def prepare_to_solve(self):
        """
        Create grids that will be used in solution stages.
        """

        # these set of grids will be used in post decision stage
        # portfolio stage and consumption stage.

        # assume for now natural borrowing constraint is less than 0
        self.zero_bound = False

        if self.zero_bound:
            self.aNrmGrid = self.aXtraGrid
        else:
            self.aNrmGrid = np.append(0.0, self.aXtraGrid)

        self.aNrmMat, self.shareMat = np.meshgrid(
            self.aNrmGrid, self.ShareGrid, indexing="ij"
        )

        # these set of grids will be used in labor stage

        self.mNrmGrid = np.append(0.0, self.aXtraGrid)

        self.mNrmMat, self.tShkMat = np.meshgrid(
            self.mNrmGrid, self.TranShkGrid, indexing="ij"
        )

        # name ShockDstn indeces
        self.PermShkIdx = 0
        self.TranShkIdx = 1
        self.RiskyShkIdx = 2

    def post_decision_stage(self, next_stage: LaborStage):
        vp_func_next = next_stage.vp_func

        def marginal_values(shocks, a_nrm, share):
            r_diff = shocks[self.RiskyShkIdx] - self.Rfree
            r_port = self.Rfree + r_diff * share
            p_shk = self.PermGroFac * shocks[self.PermShkIdx]
            t_shk = shocks[self.TranShkIdx] * np.ones_like(a_nrm)
            b_nrm_next = a_nrm * r_port / p_shk

            vP_next = p_shk ** (-self.CRRA) * vp_func_next(b_nrm_next, t_shk)

            dvda = r_port * vP_next
            dvds = a_nrm * r_diff * vP_next

            return dvda, dvds

        partials = (
            self.DiscFac
            * self.LivPrb
            * calc_expectation(
                self.ShockDstn, marginal_values, self.aNrmMat, self.shareMat
            )
        )
        partials = partials[:, :, :, 0]

        dvda = partials[0]
        dvds = partials[1]

        # make post decision dvda function

        dvda_nvrs = self.u.derinv(dvda)
        dvda_nvrs_func = BilinearInterp(dvda_nvrs, self.aNrmGrid, self.ShareGrid)
        dvda_func = MargValueFuncCRRA(dvda_nvrs_func, self.CRRA)

        # make post decision dvds function

        dvds_func = BilinearInterp(dvds, self.aNrmGrid, self.ShareGrid)

        post_decision_stage_solution = PostDecisionStage(
            dvda_func=dvda_func,
            dvds_func=dvds_func,
            dvda=dvda,
            dvds=dvds,
        )

        return post_decision_stage_solution

    def optimize_share(self, first_order_conds):
        """
        Optimization of Share on continuous interval [0,1]
        """

        # For each value of aNrm, find the value of Share such that FOC-Share == 0.
        crossing = np.logical_and(
            first_order_conds[:, 1:] <= 0.0, first_order_conds[:, :-1] >= 0.0
        )
        share_idx = np.argmax(crossing, axis=1)
        a_idx = np.arange(self.aNrmGrid.size)
        bot_s = self.ShareGrid[share_idx]
        top_s = self.ShareGrid[share_idx + 1]
        bot_f = first_order_conds[a_idx, share_idx]
        top_f = first_order_conds[a_idx, share_idx + 1]
        alpha = 1.0 - top_f / (top_f - bot_f)

        optimal_share = (1.0 - alpha) * bot_s + alpha * top_s

        # If agent wants to put more than 100% into risky asset, he is constrained
        constrained_top = first_order_conds[:, -1] > 0.0
        # Likewise if he wants to put less than 0% into risky asset
        constrained_bot = first_order_conds[:, 0] < 0.0

        # For values of aNrm at which the agent wants to put
        # more than 100% into risky asset, constrain them
        optimal_share[constrained_top] = 1.0
        optimal_share[constrained_bot] = 0.0

        if not self.zero_bound:
            # aNrm=0, so there's no way to "optimize" the portfolio
            optimal_share[0] = 1.0

        return optimal_share

    def portfolio_stage(self, next_stage: PostDecisionStage):
        optimal_share = self.optimize_share(next_stage.dvds)

        # does not include 0.0
        share_func = LinearInterp(self.aNrmGrid, optimal_share)

        dvda = next_stage.dvda_func(self.aNrmGrid, optimal_share)

        dvda_nvrs = self.u.derinv(dvda)
        dvda_nvrs_func = LinearInterp(self.aNrmGrid, dvda_nvrs)
        dvda_func = MargValueFuncCRRA(dvda_nvrs_func, self.CRRA)

        portfolio_stage_solution = PortfolioStage(
            share_func=share_func, vp_func=dvda_func, vp_vals=dvda, vp_nvrs=dvda_nvrs
        )

        return portfolio_stage_solution

    def consumption_stage(self, next_stage: PortfolioStage):
        cNrmGrid = next_stage.vp_nvrs
        mNrmGrid = self.aNrmGrid + cNrmGrid

        c_temp = np.append(0.0, cNrmGrid)
        m_temp = np.append(0.0, mNrmGrid)

        c_func = LinearInterp(m_temp, c_temp)
        vp_func = MargValueFuncCRRA(c_func, self.CRRA)

        consumption_stage_solution = ConsumptionStage(c_func=c_func, vp_func=vp_func)

        return consumption_stage_solution

    def labor_stage(self, next_stage: ConsumptionStage):
        vp_func_next = next_stage.vp_func

        mNrmMat, tShkMat = np.meshgrid(self.aNrmGrid, self.TranShkGrid, indexing="ij")

        leisure = self.n.inv(vp_func_next(mNrmMat) * tShkMat)
        leisure = np.clip(leisure, 0.0, 1.0)

        labor = 1.0 - leisure
        bNrmMat = mNrmMat - tShkMat * labor

        # if bank balances are 0, work full time
        # is this the right limit?
        labor_temp = np.insert(labor, 0, 1.0, axis=0)
        bNrmMat_temp = np.insert(bNrmMat, 0, 0.0, axis=0)

        labor_func_by_tShk = []
        for i in range(self.TranShkGrid.size):
            labor_func_by_tShk.append(
                LinearInterp(bNrmMat_temp[:, i], labor_temp[:, i])
            )

        labor_func = LinearInterpOnInterp1D(labor_func_by_tShk, self.TranShkGrid)

        vp_vals = next_stage.vp_func(mNrmMat)
        vp_vals_temp = np.insert(vp_vals, 0, 0.0, axis=0)

        dvdb_func_by_tShk = []
        for i in range(self.TranShkGrid.size):
            dvdb_func_by_tShk.append(
                LinearInterp(bNrmMat_temp[:, i], vp_vals_temp[:, i])
            )

        dvdb_func = LinearInterpOnInterp1D(dvdb_func_by_tShk, self.TranShkGrid)

        labor_stage_solution = LaborStage(labor_func=labor_func, vp_func=dvdb_func)

        return labor_stage_solution

    def calc_EndOfPrdvP(self):
        def dvdb_func(shock, bnrm):
            # This calculation is inefficient because it has to interpolate over shocks
            # because of the way this does expectations, there's no off-the-grid shocks
            # have to make sure shock and bnrm are same dimension
            return self.vp_func_next(bnrm, shock.repeat(bnrm.size))

        EndOfPrdvp_vals = calc_expectation(self.TranShkDstn, dvdb_func, self.bNrmGrid)
        EndOfPrdvp_nvrs = self.u.derinv(EndOfPrdvp_vals)
        EndOfPrdvp_nvrs_func = LinearInterp(self.bNrmGrid, EndOfPrdvp_nvrs)
        EndOfPrdvP_func = MargValueFuncCRRA(EndOfPrdvp_nvrs_func, self.CRRA)

        self.EndOfPrdvPNvrs = EndOfPrdvp_nvrs
        self.EndOfPrdvp_func = EndOfPrdvP_func

    def make_consumption_solution(self):
        # this is the consumption function that is consistent with the exogneous asset level
        # this decision comes before end of period post decision value function, but after
        # the labor-leisure decision function
        self.cGrid = self.EndOfPrdvPNvrs
        self.mGrid = self.cGrid + self.aNrmGrid

        self.c_funcEndOfPrd = LinearInterp(self.mGrid, self.cGrid)
        self.vp_funcEndOfPrd = MargValueFuncCRRA(self.c_funcEndOfPrd, self.CRRA)

    def make_labor_leisure_solution(self):
        tshkgrid = self.TranShkGrid
        zero_bound = True if tshkgrid[0] == 0.0 else False

        # this mgrid and cgrid are consistent with exogenous asset level
        mgrid = np.append(0.0, self.aXtraGrid)

        # in the previous step we found the endogenous m that is consistent with
        # exogenous asset level, now we can use m (and tshk) as the exogenous grids
        # that will give us the consistent labor, leisure, and bank balances for a
        mnrmat, tshkmat = np.meshgrid(mgrid, tshkgrid, indexing="ij")

        # this is the egm step, given exog m and tshk, find leisure
        lsrmat = self.n.inv(self.vp_funcEndOfPrd(mnrmat) * tshkmat)
        # Make sure lsrgrid is not greater than 1.0
        lsrmat = np.clip(lsrmat, 0.0, 1.0)
        if zero_bound:
            lsrmat[:, 0] = 1.0

        lbrmat = 1.0 - lsrmat  # labor is 1 - leisure
        # bank balances = cash on hand - wage * labor
        bnrmat = mnrmat - tshkmat * lbrmat

        lsrFunc_by_tShk = []
        for tShk in range(tshkgrid.size):
            lsrFunc_by_tShk.append(LinearInterp(bnrmat[:, tShk], lsrmat[:, tShk]))

        self.lsrFunc = LinearInterpOnInterp1D(lsrFunc_by_tShk, tshkgrid)

        lbrFunc_by_tShk = []
        for tShk in range(tshkgrid.size):
            lbrFunc_by_tShk.append(LinearInterp(bnrmat[:, tShk], lbrmat[:, tShk]))

        self.lbrFunc = LinearInterpOnInterp1D(lbrFunc_by_tShk, tshkgrid)

        cgrid = self.c_funcEndOfPrd(mgrid)

        # as in the terminal solution, we construct the consumption function by using
        # the c that was consistent with a, and the b that was consistent with m
        c_func_by_tShk = []
        for tShk in range(tshkgrid.size):
            c_func_by_tShk.append(LinearInterp(bnrmat[:, tShk], cgrid))

        self.c_func = LinearInterpOnInterp1D(c_func_by_tShk, tshkgrid)
        self.vp_func_now = MargValueFuncCRRA(self.c_func, self.CRRA)

    def make_consumer_labor_solution(self):
        self.solution = ConsumerLaborSolution(
            c_func=self.c_func,
            LbrFunc=self.lbrFunc,
            vp_func=self.vp_func_now,
        )

        self.solution.LsrFunc = self.lsrFunc
        self.solution.c_funcEndOfPrd = self.c_funcEndOfPrd

    def solve(self):
        labor_stage_next = self.solution_next.labor_stage

        post_decision_solution = self.post_decision_stage(labor_stage_next)
        portfolio_stage_solution = self.portfolio_stage(post_decision_solution)
        consumption_stage_solution = self.consumption_stage(portfolio_stage_solution)
        labor_stage_solution = self.labor_stage(consumption_stage_solution)

        self.solution = ConsLaborPortfolioSolution(
            post_decision_stage=post_decision_solution,
            portfolio_stage=portfolio_stage_solution,
            consumption_stage=consumption_stage_solution,
            labor_stage=labor_stage_solution,
        )

        return self.solution


init_labor_portfolio = init_labor_intensive.copy()
init_labor_portfolio.update(init_portfolio)
init_labor_portfolio["LesrCnst"] = 1.0
init_labor_portfolio["LesrShare"] = 1.0
init_labor_portfolio["UnempPrb"] = 0.0
init_labor_portfolio["DisutlLabr"] = False
init_labor_portfolio["LabrCnst"] = 0.6
init_labor_portfolio["LabrShare"] = 1.0