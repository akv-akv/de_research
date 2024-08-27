# SQLMesh exploration project

# Summary

SQLMesh is a data transformation framework that offers robust version control and automated testing.

Docs: [here](https://sqlmesh.readthedocs.io/en/stable/concepts/overview/)

# Prerequisites

Create venv and install necessary packages
```
python3 -m venv .venv
source .venv/bin/activate
pip install "sqlmesh[web]"
```

Optional for Pydantic v2
```
pip install --upgrade pydantic
pip install --upgrade pydantic-settings
```

# Example project

## Initialize project

```
mkdir sqlmesh-example
cd sqlmesh-example
sqlmesh init duckdb
```

## Plan and apply changes

```
#creates prod environment by default
sqlmesh plan

#use dev environment to run changed models and dependencies
sqlmesh plan dev
```
