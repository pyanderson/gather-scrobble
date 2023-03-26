.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 gather_scrobble

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source gather_scrobble setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/gather_scrobble.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ gather_scrobble
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

protoc:
	protoc --python_out=. --mypy_out=. ./gather_scrobble/events.proto

release: clean
	make dist
	twine upload -r gather-scrobble dist/*

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
