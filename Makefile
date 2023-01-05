test:
	pytest --cov=pytracer tests

lint:
	isort pytracer
	ruff --fix pytracer
	mypy pytracer
