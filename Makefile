test: lint
	pytest --cov=pytracer tests

lint:
	pre-commit run --all-files

coverage: test
	poetry run coverage html
	open htmlcov/index.html
