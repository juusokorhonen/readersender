EXECUTABLES = pipenv
K := $(foreach exec,$(EXECUTABLES),\
	$(if $(shell which $(exec)), ,$(error "Command '$(exec)' not found, condider installing.")))

nothing:
	echo "Nothing done."

init:
	pipenv install

dev-init:
	pipenv install --dev

setup: dev-init
	pipenv run python setup.py sdist bdist_wheel

.PHONY: tests
tests: dev-init
	pipenv run python -m pytest 

.PHONY: lint
lint: dev-init
	pipenv run python -m pytest --pep8 -m pep8