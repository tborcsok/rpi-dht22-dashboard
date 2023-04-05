import duckdb
from dotenv import load_dotenv

load_dotenv()

from webapp.environ import data_path

duckdb.sql(
    f"""
CREATE TABLE sensor_raw AS

SELECT * FROM '{data_path}/*.csv'
"""
)


duckdb.sql(
    """
CREATE TABLE sensor AS

SELECT column0 at time zone 'UTC' at time zone 'Europe/Budapest' as time,
    column1 as temp, column2 as humid FROM sensor_raw
"""
)


duckdb.sql(
    """
CREATE TABLE sensor_hourly AS

SELECT date_trunc('hour', time) as time_hourly, avg(temp) as temp, avg(humid) as humid FROM sensor
WHERE abs(temp) < 100 group by time_hourly order by time_hourly
"""
)


duckdb.sql(
    """
CREATE TABLE sensor_transformed AS

SELECT time_hourly as time, temp, humid,
AVG(temp) OVER ma as temp_ma,
AVG(humid) OVER ma as humid_ma
FROM sensor_hourly

WINDOW ma AS (
    ORDER BY "time_hourly" ASC
    RANGE BETWEEN INTERVAL 1 DAYS PRECEDING
              AND INTERVAL 1 DAYS FOLLOWING)
"""
)


duckdb.sql(
    f"""
COPY sensor_transformed TO '{data_path}/sensordata.parquet' (FORMAT PARQUET)
"""
)
