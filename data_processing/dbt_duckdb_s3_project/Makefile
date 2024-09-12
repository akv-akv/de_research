# Define variables
YEAR := 2023
START_MONTH := 01  # Set the starting month (e.g., January)
END_MONTH := 12    # Set the ending month (e.g., December)
DOCKER_IMAGE_NAME := dbt_duckdb_s3_project

# Generate a list of months based on the interval
MONTHS := $(shell seq -w $(START_MONTH) $(END_MONTH))

transform-build:
	rm ./dbt.duckdb || exit 0
	dbt build --select config.materialized:view
	docker build -t ${DOCKER_IMAGE_NAME} . \
		--build-arg dbt_third_party=dbt-duckdb \
		--build-arg commit_ref=v1.8.2

transform-build-linux:
	rm ./dbt.duckdb || exit 0
	dbt build --select config.materialized:view
	docker buildx build --platform linux/amd64 -t ${DOCKER_IMAGE_NAME} . \
		--build-arg dbt_third_party=dbt-duckdb \
		--build-arg commit_ref=v1.8.2 \
		--load

transform-bash:
	docker container run --rm -it -v ../data:/usr/app/data ${DOCKER_IMAGE_NAME} bash

transform-run-dbt-project:
	docker container run --rm -it \
		-v ./../data:/usr/app/data \
		-v ./target:/usr/app/dbt/target \
		-v ./.tmp:/usr/app/dbt/.tmp \
		${DOCKER_IMAGE_NAME} \
		dbt build --vars "{'start_date': '$(start_date)'}" --target dev-docker

transform-run-dbt-model:
	docker container run --rm -it \
		-v ../data:/usr/app/data \
		-v ./target:/usr/app/dbt/target \
		-v ./.tmp:/usr/app/dbt/.tmp \
		${DOCKER_IMAGE_NAME} \
		dbt build --vars "{'start_date': '$(start_date)'}" --target dev-docker --select $(model_name)

transform-dbt-backfill:
	@for month in $(MONTHS); do \
		start_date="$(YEAR)-$${month}-01"; \
		echo "Running backfill for month: $${start_date}"; \
		make transform-run-dbt-project start_date=$${start_date}; \
		if [ $$? -ne 0 ]; then \
			echo "dbt build failed for start_date $${start_date}"; \
			exit 1; \
		fi \
	done
	echo "Backfilling completed for months $(START_MONTH) to $(END_MONTH) in $(YEAR)"

transform-run-dbt-project-evaluator:
	docker container run --rm -it \
		-v ../data:/usr/app/data \
		-v ./target:/usr/app/dbt/target \
		-v ./.tmp:/usr/app/dbt/.tmp \
		${DOCKER_IMAGE_NAME} \
		/bin/bash -c "dbt seed && dbt deps --add-package dbt-labs/dbt_project_evaluator@0.12.0 && dbt --debug build --select package:dbt_project_evaluator --target dpe"

transform-run-dbt-limited-resources:
	docker container run --rm -it \
		-v ../data:/usr/app/data \
		-v ./target:/usr/app/dbt/target \
		-v ./.tmp:/usr/app/dbt/.tmp \
		--cpus="1" --memory="1g" --memory-swap="0" \
		${DOCKER_IMAGE_NAME} \
		dbt build --target dev-docker --vars "{'start_date': '2023-01-01'}"

transform-all: transform-build transform-run-dbt-limited-resources

docker:
	aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.eu-central-1.amazonaws.com
	docker pull $(AWS_ACCOUNT_ID).dkr.ecr.eu-central-1.amazonaws.com/${DOCKER_IMAGE_NAME}:latest
	docker container run --network host --rm -it my_container $(AWS_ACCOUNT_ID).dkr.ecr.eu-central-1.amazonaws.com/${DOCKER_IMAGE_NAME}:latest bash
