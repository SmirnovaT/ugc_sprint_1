import logging

import backoff
import clickhouse_connect
from clickhouse_connect.driver.exceptions import OperationalError
from config import ClickhouseSettings

logger = logging.getLogger("etl")

@backoff.on_exception(
    backoff.expo,
    OperationalError,
    max_tries=10,
    max_time=10,
)
def init_clickhouse(settings: ClickhouseSettings):
    logger.info("initializing clickhouse")
    client = clickhouse_connect.get_client(
        host=settings.host,
        username=settings.user,
        password=settings.password,
    )
    result = client.command(
        f"CREATE DATABASE IF NOT EXISTS {settings.database} ON CLUSTER company_cluster"
    )
    logger.info(f"create db result: {result}")
    result = client.command(
        f"CREATE TABLE IF NOT EXISTS {settings.database}.{settings.table} ON CLUSTER company_cluster (type String, "
        f"timestamp DateTime64, user_id UUID NULL, fingerprint String, element String NULL, url String NULL, "
        f"time Int NULL, id_film UUID NULL, film String NULL, original_quality Int NULL, updated_quality Int NULL, "
        f"filter String NULL) Engine=MergeTree() ORDER BY timestamp"
    )
    logger.info(f"create table result: {result}")

