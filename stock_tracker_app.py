import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import stock_tracker_plot

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
company_options = stock_tracker_plot.get_company_options()

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="colors",
            children=[
                dbc.DropdownMenuItem("Red"),
                dbc.DropdownMenuItem("Blue"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("green")
            ]
        )
    ],
    brand="Stock Plotting Tool",
    brand_href="#",
    sticky="top"
)

tickers = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='companies',
                         options=company_options,
                         value=['CVX'],
                         multi=True),
        ])
    ])
])

graph = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='stock_graph')
        ])
    ])
])

times = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.DatePickerRange(id='time_range',
                                        start_date="2017-04-30",
                                        end_date="2017-05-20",
                                        style={'align': 'center'}),
                ],
                align='center',
            )
        ],

    )
])

app.layout = html.Div(children=[
    navbar,
    tickers,
    graph,
    times
])


@app.callback(
    Output(component_id='stock_graph', component_property='figure'),
    [Input(component_id='companies', component_property='value'),
     Input(component_id='time_range', component_property='start_date'),
     Input('time_range', 'end_date')]
)
def update_stock_graph(ticker_symbols, start_time, end_time):
    print(start_time, end_time)
    stock_graph = stock_tracker_plot.plot_stocks(ticker_symbols, start_time, end_time)
    return stock_graph


if __name__ == "__main__":
    app.run_server(debug=True)
