from iexfinance import Stock
from cassandra.cluster import Cluster
from datetime import datetime
import json
import logging
import .ISIN-ticker

cluster = Cluster(['localhost'], 32774)

session = cluster.connect('iexfinance_stocks')

tsla = Stock('TSLA')

tsla_open = tsla.get_open()

print(tsla_open)

data = {}

def convertDateFormat(oldDate):
    try:
        dtobj = datetime.strptime(oldDate, '%B %d, %Y')
        newDate = datetime.strftime(dtobj, '%Y-%m-%d')
        
    except Exception as e:
        print("Error converting datetime format: " + str(e))
    finally:
        return newDate

def prepareJson(isin, ticker):
    with open('./model/insert_company.json') as json_file:
        data = json.load(json_file)
        try:
            stock = Stock(ticker)
            logging.info("Retrieving company info...")
            stock_company = stock.get_company()
            data['isin']=isin
            data['symbol']=stock_company['symbol']
            data['companyName']=stock_company['companyName']
            data['exchange']=stock_company['exchange']
            data['industry']=stock_company['industry']
            data['website']=stock_company['website']
            data['description']=stock_company['description']
            data['ceo']=stock_company['CEO']
            data['issueType']=stock_company['issueType']
            data['sector']=stock_company['sector']
            for tag in stock_company['tags']:
                data['tags'].append(tag)

            stock_eps = stock.get_earnings()
            for eps in stock_eps:
                data['eps']['actualEPS']=str(eps['actualEPS'])
                data['eps']['consensusEPS']=str(eps['consensusEPS'])
                data['eps']['estimatedEPS']=str(eps['estimatedEPS'])
                data['eps']['announceTime']=eps['announceTime']
                data['eps']['numberOfEstimates']=str(eps['numberOfEstimates'])
                data['eps']['EPSSurpriseDollar']=str(eps['EPSSurpriseDollar'])      
                data['eps']['EPSReportDate']=eps['EPSReportDate']
                data['eps']['fiscalPeriod']=eps['fiscalPeriod']
                data['eps']['fiscalEndDate']=eps['fiscalEndDate']
                data['eps']['yearAgo']=str(eps['yearAgo'])
                data['eps']['yearAgoChangePercent']=str(eps['yearAgoChangePercent'])
                data['eps']['estimatedChangePercent']=str(eps['estimatedChangePercent'])
                data['eps']['symbolId']=str(eps['symbolId'])
            
            stock_quote = stock.get_quote()
            data['highPrice']['date']=convertDateFormat(stock_quote['latestTime'])
            data['highPrice']['value']=str(stock_quote['high'])
            data['lowPrice']['date']=convertDateFormat(stock_quote['latestTime'])
            data['lowPrice']['value']=str(stock_quote['low'])
            data['closePrice']['date']=convertDateFormat(stock_quote['latestTime'])
            data['closePrice']['value']=str(stock_quote['close'])
            
        except Exception as e:
            print("Error: " + str(e))

        finally:
         return data

def insertNewCompany(data):
    addNewCoQuery = "INSERT INTO iexfinance_stocks.stocks JSON '" + json.dumps(data) + "'"
    #print(addNewCoQuery)
    rows = session.execute(addNewCoQuery)
    for row in rows:
        print(row[0])

insertNewCompany(prepareJson('US0378331005', 'AAPL'))


rows = session.execute('SELECT * FROM stocks')
for row in rows:
    print(row.isin, row.symbol)

    