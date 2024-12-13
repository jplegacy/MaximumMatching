# LaTeX Makefile
FILE=CSC-489_Book
all: $(FILE).pdf
.PHONY: clean $(FILE).pdf
clean:
	latexmk -C
$(FILE).pdf: $(FILE).tex
	echo `git rev-parse HEAD` > sha.tex
	latexmk -pdf -pdflatex="pdflatex -interactive=nonstopmode" $(FILE).tex
	rm -f sha.tex
