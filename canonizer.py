import json
import classifier
import pickle
import os
from bottle import post, request, response

canonizer_save_file_path = "data/canonizer.obj"
training_data_save_file_path = "data/train_data.json"

c = classifier.HugoClassifier()

if os.path.exists(canonizer_save_file_path):
    canonizer_file = open(canonizer_save_file_path, "rw")
    c = pickle.load(canonizer_file)

@post('/canonize')
def canonize_handler():
    '''Returns canonized form of a nomination'''
    global c

    canon_id = [0]
    try:
        try:
            for key, value in request.headers.iteritems():
                print key+":"+value

            print request.body.read()

            nomination = request.json

        except:
            raise ValueError

        if nomination is None:
            raise ValueError

        canon_id = c.canonize(nomination)

    except ValueError:
        response.status = 400
        return

    response.headers['Content_type'] = 'application/json'
    print canon_id
    return json.dumps({'canon_id': canon_id[0]})

@post('/train')
def train_handler():
    '''Trains the classifer'''

    global c
    global canonizer_save_file_path
    global training_data_save_file_path

    with open(training_data_save_file_path) as f:
        for line in f:
            nominations = json.loads(line)
            c.add_train_data(nominations)

    c.train_internal()

    canonizer_file = open(canonizer_save_file_path, "w")
    pickle.dump(c, canonizer_file)

    response.status = 200
    return

@post('/add_train_data')
def add_train_data_handler():
    '''Adds a nomination to training set'''

    global c
    global training_data_save_file_path

    try:
        try:
            nominations = request.json

        except:
            raise ValueError

        if nominations is None:
            raise ValueError

    except ValueError:
        response.status = 400
        return

    train_file = open(training_data_save_file_path,"a+")
    json.dump(nominations, train_file)
    train_file.write('\n')

    response.status = 200
    return

@post('/reset')
def reset_handler():
    '''Resets the canonizer and removes save files'''
    global c
    global canonizer_save_file_path
    global training_data_save_file_path

    os.remove(canonizer_save_file_path)
    os.remove(training_data_save_file_path)

    c = classifier.HugoClassifier()
    return