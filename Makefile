.DEFAULT_GOAL := tests
.PHONY: install-deps clean lint test cover tests

install-deps:
	pip install -r python_requirements/base.txt
	pip install -r python_requirements/test.txt

clean:
	rm -rf basest/*.py[cod] tests/*.py[cod] *.py[cod] *__pycache__*
	rm -rf basest.egg-info build dist

lint:
	flake8 basest tests setup.py stress_test.py
	isort -rc -c basest tests
	isort -c setup.py stress_test.py

test:
	coverage run --source='basest' tests/__main__.py

cover:
	coverage report -m --fail-under=100

tests: clean lint test cover

stress-test:
	python stress_test.py

package:
	python setup.py sdist bdist_wheel

release: package
	twine upload dist/*
