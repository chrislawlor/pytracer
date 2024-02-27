test:
	pytest --cov=pytracer -vv tests

lint:
	pre-commit run --all-files

coverage: test
	poetry run coverage html
	open htmlcov/index.html

profile:
	-rm pytracer.profile
	python -m cProfile -o pytracer.profile examples/world_and_camera.py -n 1
	snakeviz pytracer.profile
