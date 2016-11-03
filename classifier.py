from sklearn import tree
from sklearn.feature_extraction import FeatureHasher
import json

class HugoClassifier:
    """"Classifier for Hugo nominations"""

    # All possible fields of Hugo nominations in all categories. These
    # are used as features for the canonizer
    features = ['category', 'author', 'title', 'publisher', 'set', 'editor', 'example']

    def __init__(self):
        self.transformer = FeatureHasher(input_type="string")
        self.classifier = tree.DecisionTreeClassifier()
        self.X = []
        self.Y = []

    def train(self, X, Y) :
        """"Train the classifier.
                X: array of hugo nominations
                Y: array of corresponding canonical form ids"""

        X2 = self.transformer.transform(X)
        self.classifier = self.classifier.fit(X2, Y)


    def canonize(self, json_nomination) :
        """"Finds the ID of canonical presentation of a Hugo nomination
                nomination: Hugo nomination as JSON object
                return: Id of the canonical form
                """

        X = []
        for feature in self.features:
            if json_nomination.has_key(feature):
                X.append(json_nomination[feature])
            else:
                X.append("")

        X = [X]

        t_nom = self.transformer.transform(X)
        return self.classifier.predict(t_nom)

    def decode_hugo_nomination(self, nomination):
        ret = []
        for feature in self.features:
            if nomination.has_key(feature):
                ret.append(nomination[feature])

        return ret

    def decode_hugo_category(self, category):
        """ Decodes category entry from JSON object"""
        X = []
        Y = []

        nominations = category['nominations']
        for nom in nominations:
            nomdict = nom[0]
            nomdict['category'] = category['category']
            X.append(self.decode_hugo_nomination(nomdict))
            Y.append(nom[1])

        return X, Y

    def train_json(self, json_noms):
        """ Decodes a dictionary containing nominations in JSON format and trains the
            canonizer"""
        X = []
        Y = []
        hugo_noms = json.loads(json_noms)
        entries = hugo_noms['entries']
        for category in entries:
            decoded_category = self.decode_hugo_category(category)
            X.extend(decoded_category[0])
            Y.extend(decoded_category[1])

        self.train(X,Y)

    def add_train_data(self, nomination):
        entries = nomination['entries']
        for category in entries:
            decoded_category = self.decode_hugo_category(category)
            self.X.extend(decoded_category[0])
            self.Y.extend(decoded_category[1])

    def train_internal(self):
        self.train(self.X, self.Y)
