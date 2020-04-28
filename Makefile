EXECUTABLES = pipenv
K := $(foreach exec,$(EXECUTABLES),\
	$(if $(shell which $(exec)), ,$(error "Command '$(exec)' not found, condider installing.")))

nothing:
	echo "Nothing done."

init:
	pipenv install

dev-init:
	pipenv install --dev

.PHONY: tests
tests:
	pipenv run python -m pytest 

.PHONY: lint
lint:
	pipenv run python -m pytest --pep8 -m pep8