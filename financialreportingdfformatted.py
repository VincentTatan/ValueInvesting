import pandas as pd
from urllib import urlopen
from bs4 import BeautifulSoup
import requests

from format import format

# Getting financial reporting df
def getfinancialreportingdfformatted(ticker):

    # try:
    urlfinancials = 'http://www.marketwatch.com/investing/stock/'+ticker+'/financials'
    urlbalancesheet = 'http://www.marketwatch.com/investing/stock/'+ticker+'/financials/balance-sheet'

    text_soup_financials = BeautifulSoup(urlopen(urlfinancials).read(),"lxml") #read in
    text_soup_balancesheet = BeautifulSoup(urlopen(urlbalancesheet).read(),"lxml") #read in

    # Income statement
    titlesfinancials = text_soup_financials.findAll('td', {'class': 'rowTitle'})
    epslist=[]
    netincomelist = []
    longtermdebtlist = [] 
    interestexpenselist = []
    ebitdalist= []

    for title in titlesfinancials:
        if 'EPS (Basic)' in title.text:
            epslist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])
        if 'Net Income' in title.text:
            netincomelist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])
        if 'Interest Expense' in title.text:
            interestexpenselist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])
        if 'EBITDA' in title.text:
            ebitdalist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])


    # Balance sheet
    titlesbalancesheet = text_soup_balancesheet.findAll('td', {'class': 'rowTitle'})
    equitylist=[]
    for title in titlesbalancesheet:
        if 'Total Shareholders\' Equity' in title.text:
            equitylist.append( [td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])
        if 'Long-Term Debt' in title.text:
            longtermdebtlist.append( [td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])

    # Variables        
    eps = epslist[0]
    epsgrowth = epslist[1]
    netincome = netincomelist[0]
    shareholderequity = equitylist[0]
    roa = equitylist[1]

    longtermdebt = longtermdebtlist[0]
    interestexpense = interestexpenselist[0]
    ebitda = ebitdalist[0]
    # Don't forget to add in roe, interest coverage ratio

    ## Make it into Dataframes
    df= pd.DataFrame({'eps': eps,'epsgrowth': epsgrowth,'netincome': netincome,'shareholderequity': shareholderequity,'roa': 
                  roa,'longtermdebt': longtermdebt,'interestexpense': interestexpense,'ebitda': ebitda},index=[2012,2013,2014,2015,2016])

    # Format all the number in dataframe
    dfformatted = df.apply(format)

    # Adding roe, interest coverage ratio
    dfformatted['roe'] = dfformatted.netincome/dfformatted.shareholderequity
    dfformatted['interestcoverageratio'] = dfformatted.ebitda/dfformatted.interestexpense

#     Insert ticker and df
    return dfformatted



# This will keep tickers + gics industries & sub industries
def save_sp500_stocks_info():
    print("Come here")
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    stocks_info=[]
    tickers = []
    securities = []
    gics_industries = []
    gics_sub_industries = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        security = row.findAll('td')[1].text
        gics_industry = row.findAll('td')[3].text
        gics_sub_industry = row.findAll('td')[4].text

        tickers.append(ticker.lower())
        securities.append(security)
        gics_industries.append(gics_industry.lower())
        gics_sub_industries.append(gics_sub_industry.lower())
    
    stocks_info.append(tickers)
    stocks_info.append(securities)
    stocks_info.append(gics_industries)
    stocks_info.append(gics_sub_industries)
    
    stocks_info_df = pd.DataFrame(stocks_info).T
    stocks_info_df.columns=['tickers','security','gics_industry','gics_sub_industry']
    stocks_info_df['labels'] = stocks_info_df[['security', 'gics_industry','gics_sub_industry']].apply(lambda x: ' '.join(x), axis=1)

    # Create a list of dict based on tickers and labels
    dictlist = []
    for index, row in stocks_info_df.iterrows():
        print("there you go")
        dictlist.append({'value':row['tickers'], 'label':row['labels']})
    return dictlist
