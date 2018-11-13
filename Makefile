.PHONY: run book proper-book clean clean-proper-book pretty

run:
	python draft.py

book: clean
	python draft.py > book.md
	pandoc -s -o book.pdf book.md

proper-book: clean-proper-book
	python make_book.py
	pandoc -o the_longest_corridor.epub book/title.txt book/*.md

clean:
	rm -f book.md
	rm -f book.pdf

clean-proper-book:
	rm -f book/*.md
	rm -f the_longest_corridor.epub

pretty:
	isort
	black .
