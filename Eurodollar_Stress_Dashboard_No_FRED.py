
import dash
from dash import dcc, html
import plotly.graph_objs as go
import yfinance as yf

# FRED API key and imports are disabled in this version. Uncomment the following lines and install the library if needed.
# from fredapi import Fred
# FRED_API_KEY = 'YOUR_FRED_API_KEY'
# fred = Fred(api_key=FRED_API_KEY)

# Data without FRED API:
# Replace this with manual or mock data if needed for LIBOR-OIS Spread and SOFR
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simulated LIBOR-OIS Spread
dates = pd.date_range(end=datetime.today(), periods=180)
libor_ois_spread = pd.Series(data=np.random.uniform(0.1, 0.3, len(dates)), index=dates)

# Simulated SOFR
sofr = pd.Series(data=np.random.uniform(1.0, 1.5, len(dates)), index=dates)

# DXY (Dollar Index) from Yahoo Finance
dxy = yf.Ticker("DX-Y.NYB").history(period="6mo")  # 6 months of data
dxy_close = dxy['Close']

# Initialize Dash app
app = dash.Dash(__name__)

# Create dashboard layout
app.layout = html.Div([
    html.H1("Eurodollar Stress Dashboard (No FRED API)"),

    # LIBOR-OIS Spread
    dcc.Graph(
        id='libor-ois-spread',
        figure={
            'data': [go.Scatter(x=libor_ois_spread.index, y=libor_ois_spread, mode='lines', name='LIBOR-OIS Spread')],
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
