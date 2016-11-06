# canonizer

Canonizer is a REST service that tries to match Hugo nomination entry with a canonized form. It uses Decision Tree machine learning algorithm for matching, so it needs to be trained with a set of nominations and their correct canonized forms before usage.


## Software requirements

Following software are needed to run the canonizer. Versions listed are what the canonizer has been tested with - it might work with other versions but no guarantees.

### Software:
python 2.7.11

### Python packages:
scikit-learn 0.17.1
numpy 1.11.0
scipy 0.17.0
bottle 0.12.10 
requests 2.11.1 (Needed for running tests)

## Starting the canonizer service

From command line:
```
~/canonizer/python main.py
```
The server should start at address http://127.0.0.1:8188/


## Running tests

From command line:
```
~/canonizer/Test/python rest_tester.py
```


## REST API

### `POST /canonize`
- Parameters: `category`, `title`, `author`, `publisher`, `set`, `editor`, `example`

Returns a potential canonization id for a single nomination. Any parameter can be empty or omitted.

#### Request

```
{ "category": "Novel", "title": "3 Little Pigs", "author": "Ms Piggy", "publisher": "Example books" }
```

#### Response
```
{ "canon_id": 23 }
```
or 
400 Bad Request

### `POST /train`

Trains the canonizer with training data.

#### Response

200 OK

### `POST /add_train_data`
- Parameters: `entries` (required), `category` (required), `nominations`(required), `category`, `title`, `author`, `publisher`, `set`, `editor`, `example`, id (required for each nomination)

Adds a set of nominations to training data

#### Request

```
{
  "entries": [
     {
	"category": 'Fancast',
  	"nominations": [
    		[ { title: '3 pigs' }, 1],
    		[ { title: 'Three Little Piggies' }, 2 ]
  	]
     }
  ]
}
```

#### Response
200 OK on success
400 Bad Request in case of malformed JSON parameters

### `POST /reset`

Clears training data set and resets the canonizer.

#### Response

200 OK 

