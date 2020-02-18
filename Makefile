.PHONY: clean install dev lint flake8 pylint dist upload uploadtest test

ENV := $(shell command -v pipenv > /dev/null && echo env)
PIPRUN := $(shell command -v pipenv > /dev/null && echo pipenv run)

clean:
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.swp' -print0 | xargs -0 rm -f
	find . -name '.DS_Store' -print0 | xargs -0 rm -rf
	find . -name '__pycache__' -print0 | xargs -0 rm -rf
	-rm -rf build dist *.egg-info .eggs
	-rm -rf .tox .coverage cover
	-rm -rf Pipfile.lock
	-rm -rf .vscode
	-command -v pipenv > /dev/null && pipenv --venv > /dev/null 2>&1 && pipenv --rm

install:
	pip${ENV} install -e .

dev:
	pip${ENV} install --dev

lint: dev flake8 pylint

flake8: dev
	${PIPRUN} flake8 \
		--import-order-style google \
		--application-import-names slothstock \
		setup.py slothstock

pylint: dev
	${PIPRUN} pylint setup.py slothstock

dist: clean install
	${PIPRUN} python setup.py sdist bdist_wheel

upload:
	${PIPRUN} twine upload dist/*

uploadtest:
	${PIPRUN} twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test:
	tox
