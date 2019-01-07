#!/bin/bash
echo "Generating PDF..." 
pdflatex -jobname=howto howto.tex
bibtex howto.aux
pdflatex -jobname=howto howto.tex
pdflatex -jobname=howto howto.tex
