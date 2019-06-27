import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from financialreportingdfformatted import getfinancialreportingdf,getfinancialreportingdfformatted,save_sp500_stocks_info,save_russell_info,save_self_stocks_info
from eligibilitycheck import eligibilitycheck
from futurepricing import generate_price_df
from pandas_datareader import data as web
from datetime import datetime as dt

# Set up global variables
stockpricedf = 0
financialreportingdf =0
discountrate=0.2
margin = 0.15


# Set up the app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([

        html.H1('Value Investing'),
        # First let users choose stocks
        html.H2('Choose a stock ticker'),
        dcc.Dropdown(
            id='my-dropdown',
            options=save_sp500_stocks_info()+save_self_stocks_info(),
            value='coke'
        ),
        html.H2('5 years stocks price graph'),
        dcc.Graph(id='my-graph'),
        html.P('')

    ],style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.H2('Critical Variables and Ratios'),
        html.Table(id='my-table'),
        html.P(''),
        html.H2('Warning Flags'),
        html.Table(id='reason-list'),
        html.P('')
    ], style={'width': '55%', 'float': 'right', 'display': 'inline-block'}),
    html.H4('Discount Calculation Rate'),
    dcc.Slider(
        id='discountrate-slider',
        min=0,
        max=1,
        value=0.15,
        step=0.05,
        marks={i: '{}'.format(round(i,2)) for i in np.arange(0, 1, 0.05)}
    ),
    html.H4('Margin Calculation Rate'),
    dcc.Slider(
        id='marginrate-slider',
        min=0,
        max=1,
        value=0.15,
        step=0.05,
        marks={i: '{}'.format(round(i,2)) for i in np.arange(0, 1, 0.05)}
    ),
    html.Table(id='expected-future-price-table')
])


# For the stocks graph
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    global stockpricedf # Needed to modify global copy of stockpricedf
    stockpricedf = web.DataReader(
        selected_dropdown_value.strip(), data_source='yahoo',
        start=dt(2013, 1, 1), end=dt.now())
    return {
        'data': [{
            'x': stockpricedf.index,
            'y': stockpricedf.Close
        }]
    }


# for the table
@app.callback(Output('my-table', 'children'), [Input('my-dropdown', 'value')])
def generate_table(selected_dropdown_value,max_rows=10):
    global financialreportingdf # Needed to modify global copy of financialreportingdf
    financialreportingdf = getfinancialreportingdfformatted(selected_dropdown_value.strip().lower()).reset_index()
    financialreportingwritten = getfinancialreportingdf(selected_dropdown_value.strip()).reset_index()
    financialreportingwritten[['roe','interestcoverageratio']] = np.round(financialreportingdf[['roe','interestcoverageratio']],2)

    # Header
    return [html.Tr([html.Th(col) for col in financialreportingwritten.columns])] + [html.Tr([
        html.Td(financialreportingwritten.iloc[i][col]) for col in financialreportingwritten.columns
    ]) for i in range(min(len(financialreportingwritten), max_rows))]

    
# for the reason-list
@app.callback(Output('reason-list', 'children'), [Input('my-dropdown', 'value')])
def generate_reason_list(selected_dropdown_value):
    global financialreportingdf # Needed to modify global copy of financialreportingdf
    reasonlist = eligibilitycheck(selected_dropdown_value.strip().lower(),financialreportingdf)
    
    # Header
    return [html.Tr(html.Th('reasonlist'))] + [html.Tr(html.Td(reason)) for reason in reasonlist]


# for the expected-future-price-table
@app.callback(Output('expected-future-price-table', 'children'), 
    [Input('my-dropdown', 'value'), Input('discountrate-slider', 'value'),Input('marginrate-slider', 'value')])
def generate_future_price_table(selected_dropdown_value,discountrate,marginrate,max_rows=10):
    global financialreportingdf # Needed to modify global copy of financialreportingdf
    global stockpricedf
    pricedf = generate_price_df(selected_dropdown_value.strip(),financialreportingdf,stockpricedf,discountrate,marginrate)

    # Header
    return [html.Tr([html.Th(col) for col in pricedf.columns])] + [html.Tr([
        html.Td(html.B(pricedf.iloc[i][col]))  if col == 'decision' else html.Td(round(pricedf.iloc[i][col],2))
        for col in pricedf.columns
    ]) for i in range(min(len(pricedf), max_rows))]
    


if __name__ == '__main__':
    app.run_server(debug=True)