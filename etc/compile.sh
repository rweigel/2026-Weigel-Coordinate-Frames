PDFLATEX=/Library/TeX/texbin/pdflatex
BIBTEX=/Library/TeX/texbin/bibtex

cd ../figures/combined/
$PDFLATEX figure1.tex
$PDFLATEX figure2.tex
$PDFLATEX figure3.tex

cd ../..

$PDFLATEX submitted2-track.tex
$BIBTEX submitted2-track
$PDFLATEX submitted2-track.tex
$PDFLATEX submitted2-track.tex

$PDFLATEX submitted2.tex
$BIBTEX submitted2
$PDFLATEX submitted2.tex
$PDFLATEX submitted2.tex
