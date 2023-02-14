import dash_bootstrap_components as dbc
from dash import Input, Output, dash, dcc, html

from webapp.data import create_visualizations

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])
server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Refresh data", id="refresh-button", color="secondary"),
        # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    ],
    brand="Sensor dashboard",
    brand_href="#",
    class_name="navbar-dark bg-dark",
)

graphs = dbc.Container(
    children=[
        dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id="graph-temp", animate=True)))),
        dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id="graph-humid", animate=True)))),
    ],
    fluid="xxl",
)

app.layout = html.Div(
    [
        navbar,
        html.Div(id="graph-container", children=[graphs]),
    ]
)


@app.callback([Output("graph-temp", "figure"), Output("graph-humid", "figure")], Input("refresh-button", "n_clicks"))
def update_output_div(_):
    fig_temp, fig_humid = create_visualizations()
    return fig_temp, fig_humid
