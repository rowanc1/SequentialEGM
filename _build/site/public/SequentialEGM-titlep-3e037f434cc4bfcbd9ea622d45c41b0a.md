% -_- mode: LaTeX; TeX-PDF-mode: t; -_-
\input{./econtexRoot.texinput}\documentclass[SequentialEGM]{subfiles}
\externaldocument{\econtexRoot/SequentialEGM}
\input{\econtexRoot/Resources/owner}

\usepackage{\econtexSetup,\econark,\econtexShortcuts}

\begin{document}
% Attempted to make all lines used for Web version contain {Web} (or version with only single curly brace at end) so can be removed with sed
\ifthenelse{\boolean{Web}}{\renewcommand{\versn}{Web}}{} % {Web}

\title{EGM$^n$: The Sequential Endogenous Grid Method}
\subtitle{Solving Micro DSOPS using Unstructured Multivariate Interpolation}

\author{Alan Lujan\authNum}

\keywords{Endogenous Grid Method, Gaussian Processes, Machine Learning, Stochastic Dynamic Programming}

\jelclass{D..,E.. \par
\href{https://econ-ark.org}{\includegraphics{\ResourcesDir/PoweredByEconARK}}
}

%\date{\today}
\renewcommand{\forcedate}{February 28, 2023}\date{\forcedate}

\maketitle

\hypertarget{abstract}{}
\begin{verbatimwrite}{\econtexRoot/Subfiles/Abstract.texinput}
Heterogeneous agent models with multiple decisions are often solved using inefficient grid search methods that require many evaluations and are slow.
This paper provides a novel method for solving such models using an extension of the Endogenous Grid Method (EGM) that uses Gaussian Process Regression (GPR) to interpolate functions on unstructured grids.
First, I propose an intuitive and strategic procedure for decomposing a problem into subproblems which allows the use of efficient solution methods.
Second, using an exogenous grid of post-decision states and solving for an endogenous grid of pre-decision states that obey a first-order condition greatly speeds up the solution process.
Third, since the resulting endogenous grid can often be non-rectangular at best and unstructured at worst, GPR provides an efficient and accurate method for interpolating the value, marginal value, and decision functions.
Applied sequentially to each decision within the problem, the method is able to solve heterogeneous agent models with multiple decisions in a fraction of the time and with less computational resources than are required by standard methods currently used.
Software to reproduce these methods is available under the \href{https://econ-ark.org/}{\texttt{Econ-ARK/HARK}} project for the \texttt{python} programming language.
\end{verbatimwrite}
\input{\econtexRoot/Subfiles/Abstract.texinput}

% Various resources
\hypertarget{links}{}

\newcommand{\REMARK}{\href{https://github.com/econ-ark/REMARK}{REMARK}}
\begin{footnotesize}
\parbox{0.9\textwidth}{
\begin{center}
\begin{tabbing}
\texttt{~~~~~~~~~~~} \= \= \\
% \texttt{~~~\REMARK:~} \= \= \texttt{\url{https://econ-ark.org/materials/SequentialEGM}} \\
% \texttt{Dashboard:~} \> \> \texttt{\href{https://econ-ark.org/materials/SequentialEGM}{Click `Launch Dashboard' Button}} \\
\texttt{~~~~~~PDF:~} \> \> \texttt{\href{https://github.com/\owner/SequentialEGM/blob/master/SequentialEGM.pdf}{SequentialEGM.pdf (\textbf{Current Version})}} \\
\texttt{~~~~~html:~} \> \> \texttt{\href{https://\owner.github.io/SequentialEGM/}{https://\owner.github.io/SequentialEGM/}} \\ % Owner is defined in Resources/owner.tex
% \texttt{~~~Slides:~} \> \> \texttt{\href{https://github.com/\owner/SequentialEGM/blob/master/SequentialEGM-Slides.pdf}{SequentialEGM-Slides.pdf}} \\
\texttt{~~~GitHub:~} \> \> \texttt{\href{https://github.com/\owner/SequentialEGM}{https://github.com/\owner/SequentialEGM}} \\
\end{tabbing}
\end{center}
} % end \parbox{\textwidth}
\end{footnotesize}

\begin{authorsinfo}
\noindent \name{\href{https://quantmacro.org}{Department of Economics, The Ohio State University}, \href{mailto:alanlujan91@gmail.com}{\texttt{alanlujan91@gmail.com}}.}
\end{authorsinfo}

\pagenumbering{gobble} % Prevent numbering for pages including the TOC and title page

\ifthenelse{\boolean{Web}}{
}{
\begin{minipage}{0.9\textwidth}
\footnotesize I would like to thank Christopher D. Carroll and Simon Scheidegger for their helpful comments and suggestions. The remaining errors are my own. All figures and other numerical results were produced using the \href{https://econ-ark.org/}{\texttt{Econ-ARK/HARK}} toolkit (\cite{Carroll2018}). Additional libraries used in the production of this paper include but are not limited to: \href{https://www.scipy.org/}{\texttt{scipy}} (\cite{Virtanen2020}), \href{https://www.numpy.org/}{\texttt{numpy}} (\cite{Harris2020}), \href{https://numba.pydata.org/}{\texttt{numba}} (\cite{Lam2015}), \href{https://cupy.dev/}{\texttt{cupy}} (\cite{Okuta2017}), \href{https://scikit-learn.org/}{\texttt{scikit-learn}} (\cite{Pedregosa2011}), \href{https://pytorch.org/}{\texttt{pytorch}} (\cite{Paszke2019}), and \href{https://gpytorch.ai/}{\texttt{gpytorch}} (\cite{Gardner2018}).
\end{minipage}
} % {Web}

\titlepagefinish

\end{document}
\endinput

% \medskip\medskip
% \begin{minipage}{0.9\textwidth}
% \listoffigures
% \end{minipage}

% \medskip\medskip
% \begin{minipage}{0.9\textwidth}
% \listoftables
% \end{minipage}

%\input{\LaTeXInputs/bibliography_blend}
% Do not include appendix figures and tables in ToC unless for Web version
\ifthenelse{\boolean{Web}}{}{
\onlyinsubfile{\captionsetup[figure]{list=no}}
\onlyinsubfile{\captionsetup[table]{list=no}}
}

% \bibliography{Add-Refs,economics}
% \input{\LaTeXInputs/bibliography_blend}

\onlyinsubfile{\input{\LaTeXInputs/bibliography_blend}}

\end{document}

\endinput

% If you are editing in Emacs-AucTeX, modify the lines below for your system (otherwise ignore)
% Local Variables:
% eval: (setq TeX-command-list (assq-delete-all (car (assoc "BibTeX" TeX-command-list)) TeX-command-list))
% eval: (setq TeX-command-list (assq-delete-all (car (assoc "BibTeX" TeX-command-list)) TeX-command-list))
% eval: (setq TeX-command-list (assq-delete-all (car (assoc "BibTeX" TeX-command-list)) TeX-command-list))
% eval: (setq TeX-command-list (assq-delete-all (car (assoc "Biber" TeX-command-list)) TeX-command-list))
% eval: (add-to-list 'TeX-command-list '("BibTeX" "bibtex %s" TeX-run-BibTeX nil t :help "Run BibTeX") t)
% eval: (add-to-list 'TeX-command-list '("BibTeX" "bibtex %s" TeX-run-BibTeX nil (plain-tex-mode latex-mode doctex-mode ams-tex-mode texinfo-mode context-mode) :help "Run BibTeX") t)
% TeX-PDF-mode: t
% TeX-file-line-error: t
% TeX-debug-warnings: t
% LaTeX-command-style: (("" "%(PDF)%(latex) %(file-line-error) %(extraopts) -output-directory=. %S%(PDFout)"))
% TeX-source-correlate-mode: t
% TeX-parse-self: t
% eval: (cond ((string-equal system-type "darwin") (progn (setq TeX-view-program-list '(("Skim" "/Applications/Skim.app/Contents/SharedSupport/displayline -b %n %o %b"))))))
% eval: (cond ((string-equal system-type "gnu/linux") (progn (setq TeX-view-program-list '(("Evince" "evince --page-index=%(outpage) %o"))))))
% eval: (cond ((string-equal system-type "gnu/linux") (progn (setq TeX-view-program-selection '((output-pdf "Evince"))))))
% TeX-parse-all-errors: t
% End: