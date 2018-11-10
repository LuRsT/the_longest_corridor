run:
	python draft.py

book:
	python draft.py > book.md
	pandoc -s -o book.pdf book.md

clean:
	rm book.md
	rm book.pdf

pretty:
	isort
	black .
