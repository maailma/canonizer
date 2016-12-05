import requests
import json

addtrainurl='http://127.0.0.1:8188/add_train_data'
trainurl='http://127.0.0.1:8188/train'
canonizeurl='http://127.0.0.1:8188/canonize'
reseturl='http://127.0.0.1:8188/reset'

headers= {'Content-Type': 'application/json', 'Accept': 'text/plain'}

def do_train():
    f = open("TestData/training_data.json")

    for line in f:
        nominations = json.loads(line)
        r = requests.post(addtrainurl, json=nominations, headers=headers)

    requests.post(trainurl, headers=headers)

    f.close()

requests.post(reseturl, headers=headers)
do_train()

def run_tests():
    f = open("TestData/test_data.json")

    total = 0
    hit = 0
    miss = 0

    for line in f:
        entry = json.loads(line)
        nom = entry[0]
        id = entry[1]

        r = requests.post(canonizeurl, json=nom, headers=headers)
        jr = r.json()
        canon_id = jr["canon_id"]
        if canon_id == id:
            hit = hit + 1
        else:
            miss = miss + 1
        total = total + 1

    print "Total cases: " + str(total)
    print "Hits:   " + str(hit)
    print "Misses: " + str(miss)

print "Running tests"
run_tests()
