# %%
import logging

import duckdb
import polars as pl

from webapp.config import SKIP_PERIODS
from webapp.environ import data_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logger.info("loading csv")

sensor_raw = pl.scan_csv(f"{data_path}/*.csv", has_header=False)

logger.info("parse and clean csv")

time_col = (
    pl.col("column_1")
    .str.to_datetime("%Y-%m-%dT%H:%M:%S")
    .dt.replace_time_zone("UTC")
    .dt.convert_time_zone("Europe/Stockholm")
)
colnames = {"column_1": "time", "column_2": "temp", "column_3": "humid"}
sensor = (
    sensor_raw.with_columns(time_col)
    .rename(colnames)
    .filter(pl.col("temp").abs() < 100)
    .filter(
        *[
            ~(pl.col("time").is_between(pl.lit(p.start), pl.lit(p.end)))
            for p in SKIP_PERIODS
        ],
    )
    .collect()
)

logger.info("save cleaned sensor readings to parquet")

sensor.write_parquet(data_path / "sensordata_readings.parquet")

# %%

logger.info("aggregate")

sensor_hourly = sensor.group_by(
    pl.col("time").dt.truncate("1h"), maintain_order=True
).median()

# %%

logger.info("rolling window stats")

duckdb.sql(
    """
CREATE TABLE sensor_transformed AS

SELECT time, temp, humid,
AVG(temp) OVER ma as temp_ma,
AVG(humid) OVER ma as humid_ma
FROM sensor_hourly

WINDOW ma AS (
    ORDER BY "time" ASC
    RANGE BETWEEN INTERVAL 1 DAYS PRECEDING
              AND INTERVAL 1 DAYS FOLLOWING)
"""
)

logger.info("save aggregated data to parquet")

duckdb.sql(
    f"""
COPY sensor_transformed TO '{data_path}/sensordata.parquet' (FORMAT PARQUET)
"""
)

logger.info("done")
