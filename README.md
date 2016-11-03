# canonizer

Canonizer is a REST service that tries to match Hugo nomination entry with a canonized form. It uses Decision Tree machine learning algorithm for matching, so it needs to be trained with a set of nominations and their correct canonized forms before usage.


## Software requirements

Following software are needed to run the canonizer. Versions listed are what the canonizer has been tested with - it might work with other versions but no guarantees.

### Software:
python 2.7.11

### Python packages:
scikit-learn 0.17.1
bottle 0.12.10 


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




