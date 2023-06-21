#!/bin/bash
cd ..
# poetry config virtualenvs.create false
# export JWT_SECRET_KEY=Asdf@1234
# export JWT_REFRESH_SECRET_KEY=Asdf@12345
# export PROMETHEUS_URL=http://prometheus-stack-kube-prom-prometheus.monitoring-logging:9090
# export CLICKHOUSE_URL=chi-clickhouse-clickhouse-0-0.clickhouse
# echo $JWT_REFRESH_SECRET_KEY
# echo $JWT_SECRET_KEY
# echo $PROMETHEUS_URL
# echo $CLICKHOUSE_URL
# echo $CLICKHOUSE_USER
# echo $CLICKHOUSE_PASSWORD
nohup poetry run start
