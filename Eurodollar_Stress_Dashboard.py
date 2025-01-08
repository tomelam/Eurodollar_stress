
import dash
from dash import dcc, html
import plotly.graph_objs as go
from fredapi import Fred
import yfinance as yf

# Replace with your actual FRED API key
FRED_API_KEY = 'YOUR_FRED_API_KEY'

# Fetch data from FRED API
fred = Fred(api_key=FRED_API_KEY)

# LIBOR-OIS Spread
libor = fred.get_series('USD1MTD156N')  # Example for 1-Month USD LIBOR
ois = fred.get_series('SOFR')          # Secured Overnight Financing Rate (OIS proxy)
libor_ois_spread = libor - ois

# DXY (Dollar Index) from Yahoo Finance
dxy = yf.Ticker("DX-Y.NYB").history(period="6mo")  # 6 months of data
dxy_close = dxy['Close']

# SOFR from FRED
sofr = fred.get_series('SOFR')  # Secured Overnight Financing Rate

# Initialize Dash app
app = dash.Dash(__name__)

# Create dashboard layout
app.layout = html.Div([
    html.H1("Eurodollar Stress Dashboard"),

    # LIBOR-OIS Spread
    dcc.Graph(
        id='libor-ois-spread',
        figure={
            'data': [go.Scatter(x=libor.index, y=libor_ois_spread, mode='lines', name='LIBOR-OIS Spread')],
            'layout': go.Layout(title='LIBOR-OIS Spread', xaxis={'title': 'Date'}, yaxis={'title': 'Spread'})
        }
    ),

    # DXY Index
    dcc.Graph(
        id='dxy-index',
        figure={
            'data': [go.Scatter(x=dxy_close.index, y=dxy_close, mode='lines', name='DXY Index')],
            'layout': go.Layout(title='Dollar Index (DXY)', xaxis={'title': 'Date'}, yaxis={'title': 'Index Value'})
        }
    ),

    # SOFR
    dcc.Graph(
        id='sofr-rate',
        figure={
            'data': [go.Scatter(x=sofr.index, y=sofr, mode='lines', name='SOFR')],
            'layout': go.Layout(title='Secured Overnight Financing Rate (SOFR)', xaxis={'title': 'Date'}, yaxis={'title': 'Rate'})
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
