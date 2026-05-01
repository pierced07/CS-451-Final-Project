# Makefile for compiling the LaTeX report

PROJECT = main

all: $(PROJECT).pdf

$(PROJECT).pdf: $(PROJECT).tex references.bib
	pdflatex $(PROJECT)
	bibtex $(PROJECT)
	pdflatex $(PROJECT)
	pdflatex $(PROJECT)

clean:
	rm -f *.aux *.log *.out *.bbl *.blg *.toc *.lof *.lot *.snm *.nav *.vrb $(PROJECT).pdf
