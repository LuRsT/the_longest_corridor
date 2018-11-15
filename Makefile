.PHONY: run book proper-book clean clean-proper-book pretty clean-all

run:
	python make_book.py
	cat book/*.md

book: clean
	python make_book.py
	pandoc -o the_longest_corridor.epub book/title.txt book/*.md
	pandoc -o the_longest_corridor.pdf book/title.txt book/*.md
	cat book/*.md

clean:
	rm -f book/*.md
	rm -f the_longest_corridor.epub

pretty:
	isort
	black .
