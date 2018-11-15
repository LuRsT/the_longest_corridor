.PHONY: run book proper-book clean clean-proper-book pretty clean-all

run:
	python make_book.py
	cat book/*.md

book: clean
	python make_book.py
	pandoc --toc --top-level-division=chapter -f markdown+header_attributes -o the_longest_corridor.epub book/title.txt book/*.md
	pandoc --toc -V documentclass=report --top-level-division=chapter -o the_longest_corridor.pdf book/title.txt book/*.md
	cat book/*.md

clean:
	rm -f book/*.md
	rm -f the_longest_corridor.epub
	rm -f the_longest_corridor.pdf

pretty:
	isort
	black .
