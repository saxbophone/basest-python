.DEFAULT_GOAL := tests

.PHONY: install-deps
install-deps:
	pip install -r python_requirements/test.txt

.PHONY: clean
clean:
	rm -rf basest/*.py[cod] tests/*.py[cod] *.py[cod] *__pycache__*
	rm -rf basest.egg-info build dist

.PHONY: lint
lint:
	flake8 basest tests setup.py stress_test.py
	isort -rc -c basest tests
	isort -c setup.py stress_test.py

.PHONY: fix-lint
fix-lint:
	isort -rc basest tests
	isort setup.py stress_test.py

.PHONY: test
test:
	coverage run --source='basest' tests/__main__.py

.PHONY: cover
cover:
	coverage report -m --fail-under=100

.PHONY: tests
tests: clean lint test cover

.PHONY: stress-test
stress-test:
	python stress_test.py

.PHONY: package
package:
	python setup.py sdist bdist_wheel

.PHONY: release
release: package
	twine upload dist/*
