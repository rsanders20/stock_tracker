import plotly.express as px
import requests
import pandas as pd
import yfinance as yf
import dash_bootstrap_components as dbc


def get_company_options():
    file_path = "/home/ryan/Desktop/dev/stock_tracker/dictionaries/sp500.csv"
    ticker_df = pd.read_csv(file_path)
    ticker_df.columns = ['value', 'label']
    return ticker_df.to_dict("rows")


def plot_stocks(ticker_symbol, start_time, end_time):
    # df = get_alpha_stock_data(ticker_symbol)
    df = get_yahoo_stock_data(ticker_symbol, start_time, end_time)
    pxdf = flatten_df(df, ticker_symbol)
    # print(pxdf)
    if not pxdf.empty:
        pxdf.reset_index(level=0, inplace=True)
        graph = px.line(pxdf, x='Date', y='Close', color='ticker')

        return graph
    else:
        return px.line()


def flatten_df(df, ticker_symbol):
    if len(ticker_symbol) == 0:
        return df

    if len(ticker_symbol) == 1:
        df['ticker'] = ticker_symbol[0]
        return df

    df_list = []
    for ticker in ticker_symbol:
        individual_df = df[ticker]
        individual_df['ticker'] = ticker
        df_list.append(individual_df)
    pxdf = pd.concat(df_list)
    return pxdf


def make_ticker_string(ticker_symbol):
    if len(ticker_symbol) == 0:
        return ''

    if len(ticker_symbol) == 1:
        return ticker_symbol[0]

    ticker_symbol_str = ''
    for ticker in ticker_symbol:
        ticker_symbol_str += ticker
        ticker_symbol_str += ' '

    return ticker_symbol_str


def get_yahoo_stock_data(ticker_symbol, start_time, end_time):
    if not ticker_symbol:
        return pd.DataFrame()
    ticker_symbol_string = make_ticker_string(ticker_symbol)
    df = pd.DataFrame()

    try:
        df = yf.download(ticker_symbol_string, start=start_time, end=end_time, group_by="ticker")
    except KeyError:
        print("Key Error Caught")
    return df


def get_alpha_stock_data(ticker_symbol):
    base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
    interval="5min"
    apikey="QKIXD1S0FMPQYSPP"
    ALPHA_API = base_url+'&symbol='+ticker_symbol+'&interval='+interval+'&apikey='+apikey
    response = requests.get(ALPHA_API)
    response_json = response.json()
    print(response_json)
    if 'Error Message' not in response_json and ticker_symbol:
        df = pd.DataFrame.from_dict(response_json['Time Series (5min)']).transpose()
    else:
        df = pd.DataFrame()

    return df


if __name__ == "__main__":
    plot_stocks('CVX')
