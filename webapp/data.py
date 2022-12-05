from typing import Tuple
from plotly.graph_objs import Figure
import plotly.express as px
import pandas as pd
from pathlib import Path
import pytz
from datetime import datetime as dt, timedelta as td
from webapp.environ import data_path


localtz = pytz.timezone('Europe/Budapest')

def read_log(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, header=None)
    df.columns = ['time', 'temp', 'humid']
    df['time'] = pd.to_datetime(df['time'], utc=True)
    df['time'] = df['time'].dt.tz_convert(localtz)
    df = df.dropna()

    return df

def get_sensor_data() -> pd.DataFrame:
    files = sorted([*data_path.glob('test_log_*.csv')])
    df = pd.concat([
        read_log(p) for p in files
    ])
    df = df.set_index('time').sort_index()

    return df

def transform_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["temp"].abs()<100]

    df = df.resample("1H").mean().reset_index()

    df = df.dropna()

    return df

def create_visualizations() -> Tuple[Figure, Figure]:
    df = get_sensor_data()
    df = transform_sensor_data(df)
    df[["humid_ma", "temp_ma"]] = df.rolling("2D", on="time", center=True).mean()[["humid", "temp"]]

    fig_temp = px.line(df, 'time', ['temp', "temp_ma"], title='Hőmérséklet')
    fig_humid = px.line(df, 'time', ['humid', "humid_ma"], title='Páratartalom')

    rangeselector_opts = dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(step="all"),
        ])
    )

    fig_range = [dt.now(localtz)-td(days=7), dt.now(localtz)]

    fig_temp.update_xaxes(
        range=fig_range, 
        rangeselector=rangeselector_opts
    )

    fig_humid.update_xaxes(
        range=fig_range, 
        rangeselector=rangeselector_opts
    )
    fig_humid.update_yaxes(
        range=[0,100]
    )

    return fig_temp, fig_humid
