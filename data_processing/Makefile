transform-build:
	docker build -t akv_dbt_project . \
		--build-arg dbt_third_party=dbt-duckdb \
		--build-arg commit_ref=v1.8.2

transform-run-bash:
	docker container run --rm -it akv_dbt_project bash
