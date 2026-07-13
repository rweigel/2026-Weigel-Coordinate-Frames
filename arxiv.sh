TEX=main-submitted2.tex

rm -rf ../../arxiv
mkdir -p ../../arxiv

# Copy all files referenced in TEX to arxiv directory
cp main-submitted2.tex ../../arxiv/
cp main.bib ../../arxiv/
mkdir -p ../../arxiv/figures/combined/
cp figures/combined/*.pdf ../../arxiv/figures/combined/

# Replace \usepackage{lineno} with %\usepackage{lineno} in main.tex
sed -i '' 's/\\usepackage{lineno}/%\\usepackage{lineno}/' "$TEX"
sed -i '' 's/\\linenumbers/%\\linenumbers/' "$TEX"

cd ../..; zip -r arxiv.zip arxiv