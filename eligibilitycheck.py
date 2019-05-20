def eligibilitycheck(ticker,dfformatted):
    
    legiblestock = True
    reasonlist=[]

    # print (dfformatted)
    # EPS increases over the year (consistent)
    for growth in dfformatted.epsgrowth:
        if growth<0:
            legiblestock = False
            reasonlist.append('there is negative growth '+str(growth))
            break
    # ROE > 0.15
    if dfformatted.roe.mean()<0.13:
            legiblestock = False
            reasonlist.append('roe mean is less than 0.13 '+ str(dfformatted.roe.mean()))
    # ROA > 0.07 (also consider debt to equity cause Assets = liabilities + equity)
    if dfformatted.roa.mean()<0.07:
            legiblestock = False
            reasonlist.append('roa mean is less than 0.07 ' + str(dfformatted.roa.mean()))
    # Long term debt < 5 * income
    if dfformatted.longtermdebt.tail(1).values[0]>5*dfformatted.netincome.tail(1).values[0]:
            legiblestock = False
            reasonlist.append('longtermdebt is 5 times the netincome ')
    # Interest Coverage Ratio > 3
    if dfformatted.interestcoverageratio.tail(1).values[0]<3:
            legiblestock = False
            reasonlist.append('Interestcoverageratio is less than 3 ')
#     print ticker,legiblestock,reasonlist
    return reasonlist