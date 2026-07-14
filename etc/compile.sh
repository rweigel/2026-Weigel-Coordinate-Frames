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

sed 's/\\mbox{\\cite\([^}]*\)}/\\cite\1/g' submitted2-track.tex > submitted2.tex
#cp submitted2-track.tex submitted2.tex
sed -i '' 's/\\usepackage\[inline\]/\\usepackage[finalnew]/' submitted2.tex

$PDFLATEX submitted2.tex
$BIBTEX submitted2
$PDFLATEX submitted2.tex
$PDFLATEX submitted2.tex



