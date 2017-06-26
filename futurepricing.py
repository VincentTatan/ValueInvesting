import numpy as np
import pandas as pd



def generate_price_df(ticker,financialreportingdf,stockpricedf,discountrate,marginrate):
	dfprice = pd.DataFrame(columns =['ticker','annualgrowthrate','lasteps','futureeps'])
	pd.options.display.float_format = '{:20,.2f}'.format

	# Find EPS Annual Compounded Growth Rate
	annualgrowthrate =  financialreportingdf.epsgrowth.mean() #growth rate

	# Estimate stock price 10 years from now (Stock Price EPS * Average PE)
	lasteps = financialreportingdf.eps.tail(1).values[0] #presentvalue
	years  = 10 #period
	futureeps = abs(np.fv(annualgrowthrate,years,0,lasteps))
	dfprice.loc[0] = [ticker,annualgrowthrate,lasteps,futureeps]
	    
	dfprice.set_index('ticker',inplace=True)


	dfprice['lastshareprice']=stockpricedf.Close.tail(1).values[0]
	dfprice['peratio'] = dfprice['lastshareprice']/dfprice['lasteps']
	dfprice['futureshareprice'] = dfprice['futureeps']*dfprice['peratio']


	dfprice['presentshareprice'] = abs(np.pv(discountrate,years,0,fv=dfprice['futureshareprice']))
	dfprice['marginalizedprice'] = dfprice['presentshareprice']*(1-marginrate) 

	return dfprice