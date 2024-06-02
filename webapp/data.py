from datetime import datetime as dt
from datetime import timedelta as td
from typing import Tuple

import pandas as pd
import plotly.express as px
import plotly.io as pio
import pytz
from plotly.graph_objs import Figure

from webapp.environ import data_path

pio.templates.default = "plotly_white"

localtz = pytz.timezone("Europe/Budapest")


def get_sensor_data() -> pd.DataFrame:
    df = pd.read_parquet(data_path / "sensordata.parquet")

    return df


def create_visualizations() -> Tuple[Figure, Figure]:
    df = get_sensor_data()

    fig_temp = px.line(
        df,
        "time",
        ["temp", "temp_ma"],
        title="Temperature [°C]",
    )
    fig_humid = px.line(
        df,
        "time",
        ["humid", "humid_ma"],
        title="Relative humidity [%]",
    )

    rangeselector_opts = dict(
        buttons=list(
            [
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(step="all"),
            ]
        )
    )

    fig_range = [dt.now(localtz) - td(days=30), dt.now(localtz)]

    fig_temp.update_xaxes(range=fig_range, rangeselector=rangeselector_opts)

    fig_humid.update_xaxes(range=fig_range, rangeselector=rangeselector_opts)
    fig_humid.update_yaxes(range=[0, 100])

    for fig in [fig_temp, fig_humid]:
        fig.add_vrect(
            x0="2023-03-23",
            x1="2023-04-03",
            fillcolor="LightGray",
            opacity=1,
            line_width=0,
            annotation_text="Move",
        )

        fig.add_vrect(
            x0="2023-05-31",
            x1="2023-06-02",
            fillcolor="LightGray",
            opacity=1,
            line_width=0,
            annotation_text="Move",
        )

        fig.add_vrect(
            x0="2024-05-24",
            x1="2024-06-02",
            fillcolor="LightGray",
            opacity=1,
            line_width=0,
            annotation_text="Move",
        )

    return fig_temp, fig_humid
