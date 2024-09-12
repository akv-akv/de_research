ARG py_version=3.11.2

FROM python:$py_version-slim-bullseye AS base

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential=12.9 \
    ca-certificates=20210119 \
    git=1:2.30.2-1+deb11u2 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/*

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

RUN python -m pip install --upgrade "pip==24.0" "setuptools==69.2.0" "wheel==0.43.0" --no-cache-dir \
  && rm -rf /root/.cache/pip

FROM base AS dbt-core

ARG commit_ref=main

WORKDIR /usr/app/dbt/

RUN python -m pip install --no-cache-dir "dbt-core @ git+https://github.com/dbt-labs/dbt-core@${commit_ref}#subdirectory=core"


FROM dbt-core AS dbt-third-party

ARG dbt_third_party

RUN if [ "$dbt_third_party" ]; then \
        python -m pip install --no-cache-dir "${dbt_third_party}"; \
    else \
        echo "No third party adapter provided"; \
    fi \
  && rm -rf /root/.cache/pip

COPY ./profiles.yml /root/.dbt/profiles.yml
COPY . /usr/app/dbt
COPY ./requirements-docker.txt /usr/app/dbt/requirements.txt

RUN python -m pip install -r /usr/app/dbt/requirements.txt --no-cache-dir \
  && rm -rf /root/.cache/pip

RUN dbt deps
RUN dbt compile
