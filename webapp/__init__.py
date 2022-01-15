from dash import dash, dcc, html, Input, Output
from webapp.data import create_visualizations

app = dash.Dash(__name__)
server=app.server

app.layout = html.Div([
    html.H1("Szenzorértékek"),
    html.Div(id='graph-container', children=[
        html.Button('Refresh data', id='refresh-button'),
        dcc.Graph(id='graph-temp', animate=True),
        dcc.Graph(id='graph-humid', animate=True)
    ]),
])


@app.callback(
    [Output('graph-temp', 'figure'),
     Output('graph-humid', 'figure')],
    Input('refresh-button', 'n_clicks')
)
def update_output_div(_):
    fig_temp, fig_humid = create_visualizations()
    return fig_temp, fig_humid
