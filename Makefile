EXECUTABLES = pipenv
K := $(foreach exec,$(EXECUTABLES),\
	$(if $(shell which $(exec)), ,$(error "Command '$(exec)' not found, condider installing.")))

nothing:
	echo "Nothing done."

.PHONY: clean
clean:
	test -d dist && rm -rf dist/ || true
	test -d build && rm -rf build/ || true
	test -d readersender.egg-info && rm -rf readersender.egg-info || true
	find . -type d -name "__pycache__" -mindepth 1 -exec rm -rf {} \; -prune
	find . -type f -name "*.pyc" -exec rm {} \;
	test -f .pipenv_installed && rm .pipenv_installed || true
	test -f .pipenv_dev_installed && rm .pipenv_dev_installed || true

.pipenv_installed:
	pipenv install && touch .pipenv_installed

.pipenv_dev_installed: 
	pipenv install --dev && touch .pipenv_dev_installed

install: .pipenv_installed

dev-install: .pipenv_dev_installed

snapshot: .pipenv_dev_installed
	pipenv run python setup.py egg_info --tag-build=dev --tag-date sdist bdist_wheel bdist_egg

dist: .pipenv_dev_installed
	pipenv run python setup.py sdist bdist_wheel bdist_egg

.PHONY: tests
tests: .pipenv_dev_installed
	pipenv run python -m pytest 

.PHONY: lint
lint: .pipenv_dev_installed
	pipenv run python -m pytest --pycodestyle

.PHONY: codestyle
codestyle: .pipenv_dev_installed
	pipenv run python -m flake8 --ignore=E501