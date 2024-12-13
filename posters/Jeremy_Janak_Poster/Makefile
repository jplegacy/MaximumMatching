# LaTeX Makefile
FILE=poster
all: $(FILE).pdf
.PHONY: clean $(FILE).pdf
clean:
	latexmk -C
	rm -f poster.bbl
	rm -f poster.nav
	rm -f poster.snm
	rm -f uc_logo-eps-converted-to.pdf
	rm -f *~
$(FILE).pdf: $(FILE).tex
	latexmk -pdf -pdflatex="pdflatex -interactive=nonstopmode" $(FILE).tex