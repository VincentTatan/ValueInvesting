# ValueInvesting
For value investing dashboard
Inspired by Sean Seah Book -- Gone Fishing with (Warren Buffett)[http://www.aceprofitsacademy.com/wp-content/uploads/2016/09/Gone-Fishing-with-Buffett.pdf]


## Stocks Input Scraping
List of the companies through SP500, Russell, and self inputted
* Getting SP500 stocks info from wikipedia
* Getting russell stocks info
* Adding own list of stocks info


## Yahoo Stocks Price Scraping with Pandas DataReader
* Find the shareprice by year and the following metrics:

## Balance Sheet and Income Statement Extractions with Beautiful Soup
* EPS
* ROE
* ROA
* Long term debt
* Total Income
* Debt to Equity
* Interest Coverage Ratio

## Warning Signs List based on value investing logic
* Given list of the companies, find out the feasibility to invest
    * Been in market minimal 10 years
    * Have the track records (EPS per year)
    * Have efficiency (ROE > 15%) -- Net income / shareholder equity
    * Determine manipulation (ROA > 7%) -- Net income / Total Asset
    * Have small long term debt (Long term debt <5* total income)
    * Low Debt to Equity
    * Ability to pay interest: (Interest Coverage Ratio >3) -- EBIT / Interest expenses

## Decision Machine based on Marginal Price From Stocks EPS
* Decision making from each company in terms of return rate given the value investing methodology
    * Find EPS Annual Compounded Growth Rate
    * Estimate EPS 10 years from now
    * Estimate stock price 10 years from now (Stock Price EPS * Average PE)
    * Determine target by price today based on returns(discount rate 15%/20%)
    * Add margin of safety (Safety net 15%)
    * Buy if market price is lower than the marginal price
	* Sell if market price is higher than the marginal price

## Additional Assessments
* Qualitative Assessment of the companies
    * Advantages in business (product differentiation, branding, low price producer, high switching cost, legal barriers to entry)
    * Ability of foolhardy management (even a fool can run)
    * Avoid price competitive business