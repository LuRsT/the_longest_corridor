.PHONY: run book proper-book clean clean-proper-book pretty clean-all

run:
	python draft.py > book.md
	cat book.md

book: clean
	python draft.py > book.md
	pandoc -s -o book.pdf book.md

proper-book: clean-proper-book
	python make_book.py
	pandoc -o the_longest_corridor.epub book/title.txt book/*.md
	pandoc -o the_longest_corridor.pdf the_longest_corridor.epub

clean:
	rm -f book.md
	rm -f book.pdf

clean-proper-book:
	rm -f book/*.md
	rm -f the_longest_corridor.epub


clean-all: clean clean-proper-book


pretty:
	isort
	black .
