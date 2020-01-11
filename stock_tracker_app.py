import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import stock_tracker_plot

app = dash.Dash(__name__)

company_options = stock_tracker_plot.get_company_options()

app.layout = html.Div(children=[
    html.H1(children="Stock Plotting Tool"),

    dcc.Dropdown(id='companies',
                 options = company_options,
                 value=['CVX'],
                 multi=True),

    dcc.Graph(id='stock_graph')
])


@app.callback(
    Output(component_id='stock_graph', component_property='figure'),
    [Input(component_id='companies', component_property='value')]
)
def update_stock_graph(ticker_symbols):
    stock_graph = stock_tracker_plot.plot_stocks(ticker_symbols)
    return stock_graph


if __name__ == "__main__":
    app.run_server(debug=True)
