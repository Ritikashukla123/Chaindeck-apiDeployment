import os

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']     # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']      # should be kept secret
CLICKHOUSE_URL = os.environ['CLICKHOUSE_URL']
PROMETHEUS_URL = os.environ['PROMETHEUS_URL'] 
CLICKHOUSE_USER = os.environ['CLICKHOUSE_USER']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']
DATABASE_URL = os.environ['DATABASE_URL']
API_URL = os.environ['API_URL']