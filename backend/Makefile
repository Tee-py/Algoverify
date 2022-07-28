BLACK_CHECK_PARAMS = --diff --color --check

lint:
	isort .
	flake8
	mypy --install-types --non-interactive
	black $(BLACK_CHECK_PARAMS) ./

run-dev:
	python main.py

test:
	pytest --cov -xs