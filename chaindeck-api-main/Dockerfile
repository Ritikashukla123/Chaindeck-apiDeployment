FROM ubuntu:22.04 AS builder-image
RUN apt update -y
RUN DEBIAN_FRONTEND=noninteractive apt install git net-tools postgresql postgresql-contrib -y

# ARG SSH_PRIVATE_KEY
# RUN mkdir /root/.ssh/
# RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_ed25519

From python:3.10 as python
WORKDIR /prometheus_fast_api
FROM python as poetry
RUN apt-get install libpq-dev -y
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -

COPY . ./

RUN poetry install --no-interaction --no-ansi -vvv

WORKDIR prometheus_fast_api
COPY ./script.sh /
RUN chmod +x /script.sh
# RUN export CLICKHOUSE_URL=chi-clickhouse-clickhouse-0-0.clickhouse
ENTRYPOINT ["/script.sh"]