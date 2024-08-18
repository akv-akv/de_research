transform-build:
	docker build -t akv_dbt_project . \
		--build-arg dbt_third_party=dbt-duckdb \
		--build-arg commit_ref=v1.8.2

transform-build-linux:
	docker buildx build --platform linux/amd64 -t akv_dbt_project . \
		--build-arg dbt_third_party=dbt-duckdb \
		--build-arg commit_ref=v1.8.2 \
		--load

transform-bash:
	docker container run --rm -it -v ./data:/usr/app/data akv_dbt_project bash

transform-run-dbt:
	docker container run --rm -it \
		-v ./data:/usr/app/data \
		akv_dbt_project \
		dbt build

transform-run-dbt-project-evaluator:
	docker container run --rm -it \
		-v ./data:/usr/app/data \
		-v ./akv_dbt_project/target:/usr/app/dbt/target \
		akv_dbt_project \
		/bin/bash -c "dbt seed && dbt deps --add-package dbt-labs/dbt_project_evaluator@0.12.0 && dbt --debug build --select package:dbt_project_evaluator --target dpe"

transform-run-dbt-limited-resources:
	docker container run --rm -it \
		-v ./data:/usr/app/data \
		--cpus="1" --memory="1g" --memory-swap="1g" \
		akv_dbt_project \
		dbt build

transform-all: transform-build transform-run-dbt-limited-resources
