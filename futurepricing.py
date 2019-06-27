import numpy as np
import pandas as pd
from pandas_datareader import data as web
from datetime import datetime as dt




def generate_price_df(ticker,financialreportingdf,stockpricedf,discountrate,marginrate):
	dfprice = pd.DataFrame(columns =['ticker','annualgrowthrate','lasteps','futureeps'])
	pd.options.display.float_format = '{:20,.2f}'.format

	# Find EPS Annual Compounded Growth Rate
	# annualgrowthrate =  financialreportingdf.epsgrowth.mean() #growth rate

	try:
		print(financialreportingdf.eps.iloc[0])
		print(financialreportingdf.eps.iloc[-1])
		annualgrowthrate =  np.rate(5, 0, -1*financialreportingdf.eps.iloc[0], financialreportingdf.eps.iloc[-1])
		print(annualgrowthrate)

		# Non Conservative
		lasteps = financialreportingdf.eps.tail(1).values[0] #presentvalue

		# conservative
		# lasteps = financialreportingdf.eps.mean()

		years  = 10 #period
		futureeps = abs(np.fv(annualgrowthrate,years,0,lasteps))
		dfprice.loc[0] = [ticker,annualgrowthrate,lasteps,futureeps]
	except:
		print('eps does not exist')
	    
	dfprice.set_index('ticker',inplace=True)



	#conservative
	dfprice['peratio'] = findMinimumEPS(stockpricedf,financialreportingdf)

	dfprice['FV'] = dfprice['futureeps']*dfprice['peratio']


	dfprice['PV'] = abs(np.pv(discountrate,years,0,fv=dfprice['FV']))

	if dfprice['FV'].values[0] > 0:
		dfprice['marginprice'] = dfprice['PV']*(1-marginrate)
	else:
		dfprice['marginprice'] = 0

	dfprice['lastshareprice']=stockpricedf.Close.tail(1).values[0]

	dfprice['decision'] = np.where((dfprice['lastshareprice']<dfprice['marginprice']),'BUY','SELL')



	return dfprice


def findMinimumEPS (stockpricedf,financialreportingdf):
    # Given the share price
    finrepdf = financialreportingdf.set_index('index')
    stockpricedf['year'] = pd.DatetimeIndex(stockpricedf.index).year
    gframe = stockpricedf.groupby('year').head(1).set_index('year')
    pricebyyear = pd.DataFrame()
    pricebyyear['Close']  = gframe['Close']
    pricebyyear['eps'] = finrepdf['eps']
    pricebyyear['peratio'] = pricebyyear['Close']/pricebyyear['eps']
    return pricebyyear['peratio'].min()
