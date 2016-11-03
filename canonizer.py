import json
import classifier
from bottle import post, request, response

c = classifier.HugoClassifier()

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

    c.train_internal()
    response.status = 200
    return

@post('/add_train_data')
def add_train_data_handler():
    '''Adds a nomination to training set'''

    global c

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

    c.add_train_data(nominations)

    response.status = 200
    return

@post('/reset')
def reset_handler():
    '''Trains the canonizer'''
    global c
    c = classifier.HugoClassifier()
    return