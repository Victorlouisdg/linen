
mypy:
	mypy .

pytest:
	pytest .

pre-commit:
	pre-commit run --all-files
darglint:
	find . -name "*.py" | xargs darglint -z short -s google .



