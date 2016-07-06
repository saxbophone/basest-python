install-deps:
	pip install -r python_requirements/base.txt
	pip install -r python_requirements/test.txt

clean:
	rm -rf basest/*.py[cod]
	rm -rf tests/*.py[cod]
	rm -rf *.py[cod]

lint:
	flake8 basest tests setup.py
	isort -rc -c basest tests
	isort -c setup.py

test:
	coverage run --source='basest' tests/__main__.py

cover:
	coverage report -m --fail-under=0

tests: clean lint test cover
