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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)


# Append an externally hosted CSS stylesheet
my_css_url = "https://unpkg.com/normalize.css@5.0.0"
app.css.append_css({
    "external_url": my_css_url,
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

# Append an externally hosted JS bundle
my_js_url = 'https://unkpg.com/some-npm-package.js'
app.scripts.append_script({
    "external_url": my_js_url
})

markdown_text = '''
#### Dash and Markdown

Inspired by Sean Seah Book -- Gone Fishing with (Warren Buffett)[http://www.aceprofitsacademy.com/wp-content/uploads/2016/09/Gone-Fishing-with-Buffett.pdf]

In here we are going to try to scrape financial data:
Input: List of the companies

Web scraping: 
* Find the shareprice by year and the following metrics:
    * EPS
    * ROE
    * ROA
    * Long term debt
    * Total Income
    * Debt to Equity
    * Interest Coverage Ratio

Methods:
* Given list of the companies, find out the feasibility to invest
    * Been in market minimal 10 years
    * Have the track records (EPS per year)
    * Have efficiency (ROE > 15%) -- Net income / shareholder equity
    * Determine manipulation (ROA > 7%) -- Net income / Total Asset
    * Have small long term debt (Long term debt <5* total income)
    * Low Debt to Equity
    * Ability to pay interest: (Interest Coverage Ratio >3) -- EBIT / Interest expenses

Outputs:
* Ranking of each company in terms of return rate given the value investing methodology
    * Find EPS Annual Compounded Growth Rate
    * Estimate EPS 10 years from now
    * Estimate stock price 10 years from now (Stock Price EPS * Average PE)
    * Determine target by price today based on returns(discount rate 15%/20%)
    * Add margin of safety (Safety net 15%)

Additional:
* Qualitative Assessment of the companies
    * Advantages in business (product differentiation, branding, low price producer, high switching cost, legal barriers to entry)
    * Ability of foolhardy management (even a fool can run)
    * Avoid price competitive business    
'''

app.layout = html.Div([
    html.Div([

        html.H1('Value Investing'),
        # html.Div([
        #     dcc.Markdown(children=markdown_text)
        # ]),
        # First let users choose stocks
        html.H2('1) Choose a stock or lists of them (to be developed)'),
        dcc.Dropdown(
            id='my-dropdown',
            # options=[
            #     {'label': 'Coke', 'value': 'COKE'},
            #     {'label': 'Tesla', 'value': 'TSLA'},
            #     {'label': 'Apple', 'value': 'AAPL'}
            # ],
            options=save_sp500_stocks_info()+save_russell_info()+save_self_stocks_info(),
            value='coke'
        ),
        html.H2('2) See the 5 year trends of your stocks'),
        dcc.Graph(id='my-graph'),
        html.P('')

    ],style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.H2('3) Received data scraped from the stocks financial reporting (balancesheet, incomestatement)'),
        html.Table(id='my-table'),
        html.P(''),
        html.H2('4) Using the tips from Warren Buffett, here are the reasons why this stocks might not be suitable'),
        html.Table(id='reason-list'),
        html.P('')
    ], style={'width': '55%', 'float': 'right', 'display': 'inline-block'}),
    html.H2('5) Here are the expected future price based on discount rate and margin rate'),
    dcc.Slider(
        id='discountrate-slider',
        min=0,
        max=1,
        value=0.15,
        step=0.05,
        marks={i: '{}'.format(round(i,2)) for i in np.arange(0, 1, 0.05)}
    ),
    html.P(''),
    dcc.Slider(
        id='marginrate-slider',
        min=0,
        max=1,
        value=0.15,
        step=0.05,
        marks={i: '{}'.format(round(i,2)) for i in np.arange(0, 1, 0.05)}
    ),
    html.P(''),
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
        html.Td(round(pricedf.iloc[i][col],2)) for col in pricedf.columns
    ]) for i in range(min(len(pricedf), max_rows))]
    


if __name__ == '__main__':
    app.run_server(debug=True)