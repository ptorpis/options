from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import math
from scipy.stats import norm

# Black-Scholes formulas
def black_scholes_call(S0, X, T, r, sigma):
    d1 = (math.log(S0 / X) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return (S0 * norm.cdf(d1)) - (X * math.exp(-r * T) * norm.cdf(d2))

def black_scholes_put(S0, X, T, r, sigma):
    d1 = (math.log(S0 / X) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return (X * math.exp(-r * T) * norm.cdf(-d2)) - (S0 * norm.cdf(-d1))

# Initialize Dash app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div(id="app-container", children=[
        html.H1("Black-Scholes Option Pricing", id="title", style={'textAlign': 'center'}),

        html.Div([
            html.Label("Spot Price (S0):"),
            dcc.Input(id="spot-price", type="number", value=100, step=1, style={'width': '50%'}),

            html.Label("Strike Price (X):"),
            dcc.Input(id="strike-price", type="number", value=100, step=1, style={'width': '50%'}),

            html.Label("Time to Expiration (T in years):"),
            dcc.Input(id="time-to-expiry", type="number", value=1, step=0.01, style={'width': '50%'}),
        ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px', 'maxWidth': '400px', 'margin': 'auto', 'alignItems': 'center'}),

        html.Br(),

        html.Div([
            html.Label("Risk-Free Interest Rate (r):"),
            dcc.Slider(id="risk-free-rate", min=0, max=0.2, step=0.01, value=0.05, 
                       marks={i/100: str(i/100) for i in range(0, 21, 2)},
                       tooltip={"placement": "bottom", "always_visible": True}),

            html.Label("Volatility (σ):"),
            dcc.Slider(id="volatility", min=0.01, max=1.0, step=0.01, value=0.2, 
                       marks={i/10: str(i/10) for i in range(1, 11)},
                       tooltip={"placement": "bottom", "always_visible": True}),
        ], style={'width': '80%', 'margin': 'auto'}),

        html.Br(),

        html.Div([
            html.H2(id="call-price-output", style={'color': 'green'}),
            html.H2(id="put-price-output", style={'color': 'blue'}),
        ], style={'textAlign': 'center'})
    ], className="light-mode")  # Default theme
])


# Callback to update prices
@app.callback(
    [Output("call-price-output", "children"),
     Output("put-price-output", "children")],
    [Input("spot-price", "value"),
     Input("strike-price", "value"),
     Input("time-to-expiry", "value"),
     Input("risk-free-rate", "value"),
     Input("volatility", "value")]
)
def update_prices(S0, X, T, r, sigma):
    call_price = black_scholes_call(S0, X, T, r, sigma)
    put_price = black_scholes_put(S0, X, T, r, sigma)
    return f"Call Option Price: ${call_price:.2f}", f"Put Option Price: ${put_price:.2f}"

if __name__ == '__main__':
    app.run_server(debug=True)
