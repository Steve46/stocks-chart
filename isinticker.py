import requests
import json

url = 'https://api.openfigi.com/v1/mapping' 
header = {'Content-Type':'application/json', 'X-OPENFIGI-APIKEY':'0f7fbce8-ec94-46b8-9200-e64f6c4c49ad'} 

class SimpleStock:
    def __init__(self, isin, ticker):
        self.isin = isin
        self.ticker = ticker

def requestIsin(isin):
    try:
        with open('./model/figi-isin-request.json') as json_file:
            jDes = json.load(json_file)
            resp = []
            for i in isin:
                jDes[0]['idValue']=i
                dati= json.dumps(jDes)
                req = requests.post(url, data=dati, headers=header)
                if 'data' in req.json()[0]:
                    req_json = req.json()[0]['data']
                    for l in req_json:
                        if l['exchCode'] == i[:2]:
                            ticker = l['ticker']
                            simpleStock = SimpleStock(i, ticker)
                            resp.append(simpleStock)
                            break
                else:
                    simpleStockError = SimpleStock(i, None)
                    resp.append(simpleStockError)
            return resp
    except FileNotFoundError as fnf:
        print("{} . Il file specificato non esiste.".format(fnf))