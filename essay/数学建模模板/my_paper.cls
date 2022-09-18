\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{my_paper}[2021/08/17 My custom CV class] 
\LoadClass[12pt]{article}

\newcommand{\lunwenbiaoti}{\fontsize{15.75pt}{0}\heiti 无人机飞行的纯方位无源定位和编队调整}
\newcommand{\zhaiyao}{\fontsize{14pt}{0}\heiti 摘\quad 要}

\RequirePackage{titlesec}

\titleformat{\section}
  {\fontsize{14pt}{0}\heiti\centering}    %定义字体heiti黑体
  {}{0em}
  {}
  []

\titleformat{\subsection}
  {\heiti}    %定义字体heiti黑体
  {\bfseries\arabic{section}.\bfseries\arabic{subsection}}{1em}
  {}
  []
  
\titleformat{\subsubsection}
  {\heiti}    %定义字体heiti黑体
  {\bfseries\arabic{section}.\bfseries\arabic{subsection}.\bfseries\arabic{subsubsection}}{1em}
  {}
  []

\newenvironment{guanjianci}
  {\vspace{2ex}\noindent{\heiti 关键词:}}
  {} 
  
