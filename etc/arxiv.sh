TEX=submitted2.tex

rm -rf arxiv
mkdir -p arxiv

# Copy all files referenced in TEX to arxiv directory
cp ../"$TEX" arxiv/
cp ../agujournal2019.cls arxiv/
cp ../trackchanges.sty arxiv/
cp ../main.bib arxiv/
cp ../figures/combined/figure*.pdf arxiv/

# Replace \usepackage{lineno} with %\usepackage{lineno} in main.tex
sed -i '' 's/\\usepackage{lineno}/%\\usepackage{lineno}/' arxiv/"$TEX"
sed -i '' 's/\\linenumbers/%\\linenumbers/' arxiv/"$TEX"

zip -r arxiv.zip arxiv