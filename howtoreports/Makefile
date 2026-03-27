SHELL := /bin/bash
DOCUMENT := notes
LATEXMK := latexmk
LATEXMKOPTS := -pdf -halt-on-error -file-line-error -interaction=nonstopmode -shell-escape

all: $(DOCUMENT).pdf

$(DOCUMENT).pdf: $(DOCUMENT).tex Makefile
	set -o pipefail; $(LATEXMK) $(LATEXMKOPTS) $(DOCUMENT).tex | tee compilation.log

rebuild: clean
	$(MAKE) all

clean:
	$(LATEXMK) -C $(DOCUMENT).tex
	rm -f compilation.log

.PHONY: all rebuild clean
