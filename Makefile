# Poetry
poetry-install:
	poetry install

poetry-add-dev:
	poetry add -G dev pre-commit black isort

poetry-shell:
	poetry shell


# Pre-commit
pre-commit-install:
	pre-commit install

pre-commit-all-files:
	pre-commit run --all-files
