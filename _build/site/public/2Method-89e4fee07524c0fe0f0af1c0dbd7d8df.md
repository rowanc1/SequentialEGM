\input{./econtexRoot.texinput}
\documentclass[\econtexRoot/SequentialEGM]{subfiles}
\onlyinsubfile{\externaldocument{\econtexRoot/SequentialEGM}}
\usepackage{\econtexSetup,\econark,\econtexShortcuts}

\begin{document}

\hypertarget{method}{}
\par\section{The Sequential Endogenous Grid Method}
\notinsubfile{\label{sec:method}}

% \subsection{A basic model}

The baseline problem which I will use to demonstrate the Sequential Endogenous Grid Method (EGM$^n$) is a discrete time version of \cite{Bodie1992} where a consumer has the ability to adjust their labor as well as their consumption in response to financial risk. The objective consists of maximizing the present discounted lifetime utility of consumption and leisure.

\begin{equation}
\VFunc*0(\BLev_0, \tShkEmp_0) = \max \Ex*{t} \left[ \sum_{n = 0}^{T-t} \DiscFac^{n} \utilFunc(\CLev_{t+n}, \Leisure_{t+n}) \right]
\end{equation}

In particular, this example makes use of a utility function that is based on Example 1 in the paper, which is that of additively separable utility of labor and leisure as

\begin{equation}
\utilFunc(\CLev, \Leisure) = \util(\CLev) + \h(\Leisure) = \frac{C^{1-\CRRA}}{1-\CRRA} + \labShare^{1-\CRRA} \frac{\Leisure^{1-\leiShare}}{1-\leiShare}
\end{equation}

where the term $\labShare^{1-\CRRA}$ is introduced to allow for a balanced growth path as in \cite{Mertens2011}. The use of additively separable utility is ad-hoc, as it will allow for the use of multiple EGM steps in the solution process, as we'll see later.

This model represents a consumer who begins the period with a level of bank balances $\bRat_{t}$ and a given wage offer $\tShkEmp_{t}$. Simultaneously, they are able to choose consumption, labor intensity, and a risky portfolio share with the objective of maximizing their utility of consumption and leisure, as well as their future wealth.

The problem can be written in normalized recursive form\footnote{
As in \cite{Carroll2009}, where the utility of normalized consumption and leisure is defined as

\begin{equation}
\utilFunc(\cRat*{t}, \leisure*{t}) = \PLev*{t}^{1-\CRRA} \frac{\cRat*{t}^{1-\CRRA}}{1-\CRRA} + (\labShare\PLev*{t})^{1-\CRRA} \frac{\leisure*{t}^{1-\leiShare}}{1-\leiShare}
\end{equation}

} as

\begin{equation}
\begin{split}
\vFunc*{t}(\bRat*{t}, \tShkEmp*{t}) & = \max*{\{\cRat*{t},
\leisure*{t}, \riskyshare*{t}\}} \utilFunc(\cRat*{t}, \leisure*{t}) +
\DiscFac \Ex*{t} \left[ \PGro_{t+1}^{1-\CRRA}
\vFunc_{t+1} (\bRat_{t+1},
\tShkEmp_{t+1}) \right] \\
& \text{s.t.} \\
\labor*{t} & = 1 - \leisure*{t} \\
\mRat*{t} & = \bRat*{t} + \tShkEmp*{t}\labor*{t} \\
\aRat*{t} & = \mRat*{t} - \cRat*{t} \\
\Rport*{t+1} & = \Rfree + (\Risky*{t+1} - \Rfree)
\riskyshare*{t} \\
\bRat*{t+1} & = \aRat*{t} \Rport*{t+1} / \PGro*{t+1}
\end{split}
\end{equation}

in which $\labor_{t}$ is the time supplied to labor net of leisure, $\mRat_{t}$ is the market resources totaling bank balances and labor income, $\aRat_{t}$ is the amount of saving assets held by the consumer, and $\riskyshare_{t}$ is the risky share of assets, which induce a $\Rport_{t+1}$ return on portfolio that results in next period's bank balances $\bRat_{t+1}$ normalized by next period's permanent income $\PGro_{t+1}$.

% \begin{equation}
% \begin{split}
% \vFunc*{t}(\bRat*{t}, \tShkEmp*{t}) & = \max*{\cRat*{t},
% \leisure*{t}} \util(\cRat*{t}) + \h(\leisure*{t}) +
% \vEnd*{t} (\aRat*{t})
% \\
% & \text{s.t.} \\
% \labor*{t} & = 1 - \leisure*{t} \\
% \mRat*{t} & = \bRat*{t} + \tShkEmp*{t}\labor*{t} \\
% \aRat*{t} & = \mRat*{t} - \cRat\_{t} \\
% \end{split}
% \end{equation}

\subsection{Restating the problem sequentially}

We can make a few choices to create a sequential problem which will allow us to use multiple EGM steps in succession. First, the
agent decides their labor-leisure trade-off and receives a wage. Their wage
plus their previous bank balance then becomes their market resources. Second, given
market resources, the agent makes a pure consumption-saving decision. Finally, given an amount of savings, the consumer then decides their risky portfolio share.

Starting from the beginning of the period, we can define the labor-leisure problem as

\begin{equation}
\begin{split}
\vFunc*{t}(\bRat*{t}, \tShkEmp*{t}) & = \max*{ \leisure*{t}}
\h(\leisure*{t}) + \vOpt*{t} (\mRat*{t}) \\
& \text{s.t.} \\
0 & \leq \leisure*{t} \leq 1 \\
\labor*{t} & = 1 - \leisure*{t} \\
\mRat*{t} & = \bRat*{t} + \tShkEmp*{t}\labor\_{t}.
\end{split}
\end{equation}

The pure consumption-saving problem is then

\begin{equation}
\begin{split}
\vOpt*{t}(\mRat*{t}) & = \max*{\cRat*{t}} \util(\cRat*{t}) + \DiscFac\vEnd*{t}(\aRat*{t}) \\
& \text{s.t.} \\
0 & \leq \cRat*{t} \leq \mRat*{t} \\
\aRat*{t} & = \mRat*{t} - \cRat*{t}.
\end{split}
\end{equation}

Finally, the risky portfolio problem is

\begin{equation}
\begin{split}
\vEnd*{t}(\aRat*{t}) & = \max*{\riskyshare*{t}}
\Ex*{t} \left[ \PGro*{t+1}^{1-\CRRA}
\vFunc*{t+1}(\bRat*{t+1},
\tShkEmp*{t+1}) \right] \\
& \text{s.t.} \\
0 & \leq \riskyshare*{t} \leq 1 \\
\Rport*{t+1} & = \Rfree + (\Risky*{t+1} - \Rfree)
\riskyshare*{t} \\
\bRat*{t+1} & = \aRat*{t} \Rport*{t+1} / \PGro\_{t+1}.
\end{split}
\end{equation}

This sequential approach is explicitly modeled after the nested approaches explored in \cite{Clausen2020} and \cite{Druedahl2021}. However, I will offer additional insights that expand on these methods. An important observation is that now, every single choice is self-contained in a subproblem, and although the structure is specifically chosen to minimize the number of state variables at every stage, the problem does not change by this structural imposition. This is because there is no additional information or realization of uncertainty that happens between decisions, as can be seen by the expectation operator being in the last subproblem. From the perspective of the consumer, these decisions are essentially simultaneous, but a careful organization into sub-period problems enables us to solve the model more efficiently and can provide key economic insights. In this problem, as we will see, a key insight will be the ability to explicitly calculate the marginal value of wealth and the Frisch elasticity of labor.

%\begin{equation}
% \begin{split}
% \vFunc*{t}(\bRat*{t}) & = \max*{ \labor*{t}} \h(\leisure*{t}) + \Ex*{t} \left[ \vOpt_{t} (\mRat_{t}) \right] \\
% & \text{s.t.} \\
% \labor*{t} & = 1 - \leisure*{t} \\
% \mRat*{t} & = \bRat*{t} + \tShkEmp*{t+1}\labor*{t} \\
% \end{split}
%\end{equation}
%
%\begin{equation}
% \begin{split}
% \vOpt*{t}(\mRat*{t}) & = \max*{\aRat*{t}} \util(\cRat*{t}) + \DiscFac \Ex*{t} \left[ \PGro_{t+1}^{1-\CRRA} \vFunc_{t+1} (\bRat_{t+1}) \right] \\
% & \text{s.t.} \\
% \aRat*{t} & = \mRat*{t} - \cRat*{t} \\
% \bRat*{t+1} & = \aRat*{t} \Rfree / \PGro*{t+1}
% \end{split}
%\end{equation}

\subsection{The portfolio decision subproblem}

As useful as it is to be able to use the EGM step more than once, there are clear problems where the EGM step is not applicable. This basic labor-portfolio choice problem demonstrates where we can use an additional EGM step, and where we can not. First, we go over a subproblem where we can not use the EGM step.

In reorganizing the labor-portfolio problem into subproblems, we assigned the utility of leisure to the leisure-labor subproblem and the utility of consumption to the consumption-savings subproblem. There are no more separable convex utility functions to assign to this problem, and even if we re-organized the problem in a way that moved one of the utility functions into this subproblem, they would not be useful in solving this subproblem via EGM as there is no direct relation between the risky share of portfolio and consumption or leisure. Therefore, the only way to solve this subproblem is through standard convex optimization and root-finding techniques.

Restating the problem in compact form gives

\begin{equation}
\vEnd*{t}(\aRat*{t}) = \max*{\riskyshare*{t}} \Ex*{t} \left[ \PGro*{t+1}^{1-\CRRA}
\vFunc*{t+1}\left(\aRat*{t}(\Rfree + (\Risky*{t+1} - \Rfree) \riskyshare*{t}), \tShkEmp\_{t+1}\right)
\right].
\end{equation}

The first-order condition with respect to the risky portfolio share is then

\begin{equation}
\Ex*{t} \left[ \PGro*{t+1}^{-\CRRA} \vFunc*{t+1}^{\bRat}\left(\bRat*{t+1}, \tShkEmp*{t+1}\right) (\Risky*{t+1} - \Rfree) \right] = 0.
\end{equation}

Finding the optimal risky share requires numerical optimization and root-solving of the first-order condition. To close out the problem, we can calculate the envelope condition as

\begin{equation}
\vEnd*{t}'(\aRat*{t}) = \Ex*{t} \left[ \PGro*{t+1}^{-\CRRA} \vFunc*{t+1}^{\bRat}\left(\bRat*{t+1}, \tShkEmp*{t+1}\right) \Rport*{t+1} \right].
\end{equation}

\subsubsection{A note on avoiding taking expectations more than once.}

We could instead define the portfolio choice subproblem as:

\begin{equation}
\vEnd*{t}(\aRat*{t}) = \max*{\riskyshare*{t}} \vOptAlt(\aRat*{t}, \riskyshare*{t})
\end{equation}

where

\begin{equation}
\begin{split}
\vOptAlt*{t}(\aRat*{t}, \riskyshare*{t}) & = \Ex*{t} \left[ \PGro_{t+1}^{1-\CRRA} \vFunc_{t+1}\left(\bRat_{t+1}, \tShkEmp_{t+1}\right) \right] \\
\Rport*{t+1} & = \Rfree + (\Risky*{t+1} - \Rfree) \riskyshare*{t} \\
\bRat*{t+1} & = \aRat*{t} \Rport*{t+1} / \PGro\_{t+1}
\end{split}
\end{equation}

In this case, the process is similar. The only difference is that we don't have to take expectations more than once. Given the next period's solution, we can calculate the marginal value functions as:

\begin{equation}
\begin{split}
\vOptAlt*{t}^{\aRat}(\aRat*{t}, \riskyshare*{t}) & = \Ex*{t} \left[ \PGro_{t+1}^{-\CRRA} \vFunc_{t+1}'\left(\bRat_{t+1}, \tShkEmp_{t+1}\right) \Rport_{t+1} \right] \\
\vOptAlt*{t}^{\riskyshare}(\aRat*{t}, \riskyshare*{t}) & = \Ex*{t} \left[ \PGro_{t+1}^{-\CRRA} \vFunc_{t+1}'\left(\bRat_{t+1}, \tShkEmp_{t+1}\right) \aRat_{t} (\Risky_{t+1} - \Rfree) \right] \\
\end{split}
\end{equation}

If we are clever, we can calculate both of these in one step. Now, the optimal risky share can be found by the first-order condition and we can use it to evaluate the envelope condition.

\begin{equation}
\text{F.O.C.:} \qquad \vOptAlt*{t}^{\riskyshare}(\aRat*{t}, \riskyshare*{t}^{\*}) = 0 \qquad
\text{E.C.:} \qquad \vEnd*{t}^{\aRat}(\aRat*{t}) = \vOptAlt*{t}^{\aRat}(\aRat*{t}, \riskyshare*{t}^{\*})
\end{equation}

\subsection{The consumption-saving subproblem}

The consumption-saving EGM follows \cite{Carroll2006} but I will cover it for exposition. We can begin the solution process by restating the consumption-savings subproblem in a more compact form, substituting the market resources constraint and ignoring the no-borrowing constraint for now. The problem is:

\begin{equation}
\vOpt*{t}(\mRat*{t}) = \max*{\cRat*{t}} \util(\cRat*{t}) +
\DiscFac \vEnd*{t}(\mRat*{t}-\cRat*{t})
\end{equation}

To solve, we derive the first-order condition with respect to $\cRat_{t}$ which gives the familiar Euler equation:

\begin{equation}
\utilFunc'(\cRat*t) = \DiscFac \vEnd*{t}'(\mRat*{t} - \cRat*{t}) = \DiscFac
\vEnd*{t}'(\aRat*{t})
\end{equation}

Inverting the above equation is the (first) EGM step.

\begin{equation}
\cEndFunc*{t}(\aRat*{t}) = \utilFunc'^{-1}\left( \DiscFac \vEnd*{t}'(\aRat*{t})
\right)
\end{equation}

Given the utility function above, the marginal utility of consumption and its inverse are

\begin{equation}
\utilFunc'(\cRat) = \cRat^{-\CRRA} \qquad \utilFunc'^{-1}(\xRat) =
\xRat^{-1/\CRRA}.
\end{equation}

\cite{Carroll2006} demonstrates that by using an exogenous grid of $\aMat$ points we can find the unique
$\cEndFunc_{t}(\aMat)$ that optimizes the consumption-saving problem, since the first-order condition is necessary and sufficient.
Further, using the market resources constraint, we can recover the exact amount
of market resources that is consistent with this consumption-saving decision as

\begin{equation}
\mEndFunc*{t}(\aMat) = \cEndFunc*{t}(\aMat) + \aMat.
\end{equation}

This $\mEndFunc_{t}(\aMat)$ is the ``endogenous'' grid that is consistent
with the exogenous decision grid $\aMat$. Now that we have a
$(\mEndFunc_{t}(\aMat), \cEndFunc_{t}(\aMat))$ pair for each
$\aRat \in \aMat$, we can construct an interpolating consumption function for
market resources points that are off-the-grid.

The envelope condition will be useful in the next section, but for completeness
is defined here.

\begin{equation}
\vOpt*{t}'(\mRat*{t}) = \DiscFac \vEnd*{t}'(\aRat*{t}) = \utilFunc'(\cRat\_{t})
\end{equation}

\subsection{The labor-leisure subproblem}

The labor-leisure subproblem can be restated more compactly as:

\begin{equation}
\vFunc*{t}(\bRat*{t}, \tShkEmp*{t}) = \max*{ \leisure*{t}}
\h(\leisure*{t}) + \vOpt*{t}(\bRat*{t} +
\tShkEmp*{t}(1-\leisure*{t}))
\end{equation}

The first-order condition with respect to leisure implies the labor-leisure Euler equation

\begin{equation}
\h'(\leisure*{t}) = \vOpt*{t}'(\mRat*{t}) \tShkEmp*{t}
\end{equation}

The marginal utility of leisure and its inverse are

\begin{equation}
\h'(\leisure) = \labShare\leisure^{-\leiShare} \qquad
\h'^{-1}(\xRat) = (\xRat/\labShare)^{-1/\leiShare}
\end{equation}

Using an exogenous grid of $\mMat$ and $\tShkMat$, we can find leisure as

\begin{equation}
\zEndFunc*{t}(\mMat, \tShkMat) = \h'^{-1}\left(
\vOpt*{t}'(\mMat) \tShkMat \right)
\end{equation}

In this case, it's important to note that there are conditions for leisure itself. An agent with a small level of market resources $\mRat_{t}$ might want to work more than their available time endowment, especially at higher levels of income $\tShkEmp_{t}$, if the utility of leisure is not enough to compensate for their low wealth. In these situations, the optimal unconstrained leisure might be negative, so we must impose a constraint on the optimal leisure function. This is similar to the treatment of an artificial borrowing constraint in the pure consumption subproblem. From now on, let's call this constrained optimal function $\hat{\zEndFunc}_{t}(\mMat, \tShkMat)$, where

\begin{equation}
\hat{\zEndFunc}_{t}(\mMat, \tShkMat) = \max \left[ \min \left[ \zEndFunc_{t}(\mMat, \tShkMat), 1 \right], 0 \right]
\end{equation}

Then, we derive labor as $\lEndFunc_{t}(\mRat_{t}, \tShkEmp_{t}) = 1 -
  \hat{\zEndFunc}_{t}(\mRat_{t}, \tShkEmp_{t})$. Finally, for each
$\tShkEmp_{t}$ and
$\mRat_{t}$ as an exogenous grid, we can find the endogenous grid of bank
balances as $\bEndFunc_{t}(\mRat_{t}, \tShkEmp_{t}) = \mRat_{t} -
  \tShkEmp_{t}\lEndFunc_{t}(\mRat_{t}, \tShkEmp_{t})$.

The envelope condition then provides a heterogeneous Frisch elasticity of labor as simply

\begin{equation}
\vFunc*{t}^{b}(\bRat*{t}, \tShkEmp*{t}) = \vOpt*{t}'(\mRat*{t}) =
\h'(\leisure*{t})/\tShkEmp\_{t}.
\end{equation}

\subsection{Curvilinear Grids}

Although EGM$^n$ seems to be a simple approach, there is one important caveat that we have not discussed, which is the details of the interpolation. In the pure consumption-savings problem, a one-dimensional exogenous grid of post-decision liquid assets $\aMat$ results in a one-dimensional endogenous grid of total market resources $\mMat$. However, as we know from standard EGM, the spacing in the $\mMat$ grid is different from the spacing in the $\aMat$ grid as the inverted Euler equation is non-linear. This is no problem in a one-dimensional problem as we can simply use non-uniform linear interpolation.

However, the same is true of higher dimensional problems, where the exogenous grid gets mapped to a warped endogenous grid. In this case, it is not possible to use standard multi-linear interpolation, as the resulting endogenous grid is not rectilinear. Instead, I introduce a novel approach to interpolation that I call Warped Grid Interpolation (WGI), which is similar to \cite{White2015}'s approach but computationally more efficient and robust. The details of this interpolation method will be further explained in Section~\ref{sec:gpr}, but for now, we show the resulting warped endogenous grid for the labor-leisure problem.

% TODO: Add figure

\subsection{Alternative Parametrization}

An alternative formulation for the utility of leisure is to state it in terms
of the disutility of labor as in (references)

\begin{equation}
\h(\labor) = - \leiShare \frac{\labor^{1+\labShare}}{1+\labShare}
\end{equation}

In this case, we can restate the problem as

\begin{equation}
\h(\leisure) = - \leiShare
\frac{(1-\leisure)^{1+\labShare}}{1+\labShare}
\end{equation}

The marginal utility of leisure and its inverse are

\begin{equation}
\h'(\leisure) = \leiShare(1-\leisure)^{\labShare} \qquad
\h'^{-1}(\xRat) = 1 - (\xRat/\leiShare)^{1/\labShare}
\end{equation}

\onlyinsubfile{\input{\LaTeXInputs/bibliography_blend}}

\ifthenelse{\boolean{Web}}{}{
\onlyinsubfile{\captionsetup[figure]{list=no}}
\onlyinsubfile{\captionsetup[table]{list=no}}
\end{document} \endinput
}