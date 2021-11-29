
# %%

import plotly.express as px
import pandas as pd
import pytz
from pathlib import Path

def read_log(filename: str):
    df = pd.read_csv(filename, header=None)
    df.columns = ['time', 'temp', 'humid']
    df['time'] = pd.to_datetime(df['time'])
    df['time'] = df['time'].dt.tz_localize(pytz.timezone('UTC'))
    df['time_local'] = df['time'].dt.tz_convert(pytz.timezone('Europe/Budapest'))
    df = df.dropna()

    return df

files = sorted([*Path('.').glob('test_log_*.csv')])
df = pd.concat([
    read_log(p) for p in files
])
df = df.sort_values('time')
df[['temp_rolling', 'humid_rolling']] = df[['temp', 'humid']].rolling(9, center=True).median()
df = df.dropna()


# %%

px.line(df, 'time_local', 'humid_rolling')

# %%

px.line(df, 'temp_rolling', 'humid_rolling')


# %%

df_hourly_mean = df.groupby(df.time.dt.hour).mean().reset_index()

# %%

px.line(df_hourly_mean, 'time', 'temp_rolling')

# %%

px.line(df_hourly_mean, 'time', 'humid_rolling')

# %%
