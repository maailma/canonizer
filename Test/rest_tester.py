import requests
import json

addtrainurl='http://127.0.0.1:8188/add_train_data'
trainurl='http://127.0.0.1:8188/train'
canonizeurl='http://127.0.0.1:8188/canonize'

headers= {'Content-Type': 'application/json', 'Accept': 'text/plain'}

f = open("HugoTestData1.json")
s = f.read();
nominations = json.loads(s)

r = requests.post(addtrainurl, json=nominations, headers=headers)
r = requests.post(trainurl, headers=headers)

testnom = { "category": "Novel", "title": "Ancillary Justice", "author": "Ann Lecklie", "publisher": "Orbit Books" }
r = requests.post(canonizeurl, json=testnom, headers=headers)
print r.json()
