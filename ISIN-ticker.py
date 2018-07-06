import requests 
import json

url = 'https://api.openfigi.com/v1/mapping' 
headers = {'Content-Type':'application/json', 'X-OPENFIGI-APIKEY':'0f7fbce8-ec94-46b8-9200-e64f6c4c49ad'} 

def requestIsin(isin):
    with open('./model/figi-isin-request.json') as json_file:
        jDes = json.load(json_file)
        for i in isin:
            try:
                jDes[0]['idValue']=i
                print(jDes)
                req = requests.post(url, json=jDes, headers=headers )
                print(req.json())

            except Exception as e:
                print("Error: " + str(e))

            finally:
                return "Data requested"

print(requestIsin(["US0378331005", "US88160R1014"]))
