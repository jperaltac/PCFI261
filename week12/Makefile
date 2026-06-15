SHELL := /bin/bash

DOCUMENT=notes
LATEXOPTS=-halt-on-error -file-line-error -shell-escape

all: $(DOCUMENT).pdf

$(DOCUMENT).pdf: $(DOCUMENT).tex
	set -o pipefail; pdflatex $(LATEXOPTS) $(DOCUMENT).tex | tee compilation.log
	set -o pipefail; pdflatex $(LATEXOPTS) $(DOCUMENT).tex | tee compilation.log

clean:
	rm -f $(DOCUMENT).pdf $(DOCUMENT).dvi *.aux *.log *.bbl *.blg *Notes.bib *.out *.snm *.toc *.nav *.vrb
	rm -fr _minted

check:
	aspell -t list < $(DOCUMENT).tex | sort | uniq

.PHONY: clean check
