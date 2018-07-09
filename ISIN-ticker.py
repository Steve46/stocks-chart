import requests
import json

url = 'https://api.openfigi.com/v1/mapping' 
header = {'Content-Type':'application/json', 'X-OPENFIGI-APIKEY':'0f7fbce8-ec94-46b8-9200-e64f6c4c49ad'} 

def requestIsin(isin):
    try:
        with open('./model/figi-isin-request.json') as json_file:
            jDes = json.load(json_file)
            resp = []
            for i in isin:
                jDes[0]['idValue']=i
                dati= json.dumps(jDes)
                print(dati)
                req = requests.post(url, data=dati, headers=header)
                #print(req.json())
                c = 0
                for l in req.json()[0]['data']:
                    if l['exchCode'] == isin[c][:2]:
                        c += 1
                        ticker = l['ticker']
                        resp.append(ticker)
                        print(resp)
    except FileNotFoundError as fnf:
        print("{} . Il file specificato non esiste.".format(fnf))

print(requestIsin(["US0378331005", "US88160R10134"]))