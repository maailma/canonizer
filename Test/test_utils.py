import json
import random
import classifier

category_encoding = ["novel", "novella", "novelette", "short story", "non-fiction", "dramatic presentation",
                     "pro editor", "pro artist", "semiprozine", "fanzine", "fan writer", "fan artist", "Campbell Award"]

features = ['category', 'author', 'title', 'publisher', 'set', 'editor', 'example']

def read_entry(entry_str):
    """ Reads a hugo 1984 original data entry and converts it into JSON object"""
    # Hugo 1984 data format
    file_format = {"category": (6, 8), "title": (27, 74), "originalcategory": (75, 76), "author": (77, 111),
                   "publisher": (112, 132)}

    category = entry_str[file_format["category"][0]: file_format["category"][1]]
    title = entry_str[file_format["title"][0]: file_format["title"][1]]
    original_cat = entry_str[file_format["originalcategory"][0]: file_format["originalcategory"][1]]
    author = entry_str[file_format["author"][0]: file_format["author"][1]]
    publisher = entry_str[file_format["publisher"][0]: file_format["publisher"][1]]

    return {"category": category, "title": title, "author": author, "publisher": publisher, "original_cat": original_cat}

def split_data(input_file, first_output, second_output, probability) :
    """ Splits a file line by line. Probability parameter determines the ratio of the split """
    fst_file = open(first_output, "w")
    scnd_file = open(second_output, "w")
    original_data = open(input_file, "r")

    for line in original_data:
        rnd = random.random()
        if rnd < probability:
            fst_file.writelines(line)
        else:
            scnd_file.writelines(line)

def convert_json_entry_to_training_data(traindata, jsonentry):
    """ Converts a single JSON entry into 2017 Hugo JSON format """
    train_entry = {}

    for f in features:
        if f in jsonentry:
            train_entry[f] = jsonentry[f]

    cat = train_entry['category']
    del train_entry['category']
    cat = category_encoding[int(cat)-1]
    trentry_canon = [train_entry, 0]

    for entry in traindata['entries']:
        if cat == entry['category']:
            entry['nominations'].append(trentry_canon)
            return

    traindata['entries'].append({"category": cat, "nominations":[trentry_canon]})

def convert_json_entry_to_nomination(jsonentry):
    """ Converts Hugo 1984 JSON entry to Hugo 2017 JSON entry format """
    nomination = {}
    for f in features:
        if f in jsonentry:
            nomination[f] = jsonentry[f]

    nomination['category'] = jsonentry['original_cat']
    nomination['category'] = category_encoding[int(nomination['category'])-1]
    return nomination

def convert_txt_to_json(input_file, output_file) :
    """ Converts Hugo 1984 entry file into JSON format and writes the JSON entries into output file """
    inpf = open(input_file, "r")
    outf = open(output_file, "w")

    for line in inpf:
        entry = read_entry(line)
        for k in entry:
            if isinstance(entry[k],basestring):
                entry[k] = str.strip(entry[k])
        json.dump(entry,outf)
        outf.write("\n")

def convert_json_file_to_nomination_file(input_file, output_file):
    """ Converts file of JSON entries into canonizer training data format """
    inpf = open(input_file, "r")
    outf = open(output_file, "w")

    tr = {"entries": []}
    for line in inpf:
        print line
        json_entry = json.loads(line)
        convert_json_entry_to_training_data(tr, json_entry)

    print tr
    json.dump(tr, outf)

def pre_process_training_data(input_file, output_file):
    """ Assigns canonization IDs to training data set entries.
        IDs are rolling index, starting from 1.
        Canonization is done based on title, so mistyped
        titles will result in extra canonization ID.
    """

    id = 0
    last_title = ""
    inpf = open(input_file, "r")
    outf = open(output_file, "w")

    json_input = json.load(inpf)

    for entry in json_input["entries"]:
        for nom in entry["nominations"]:
            if nom[0]["title"] != last_title:
                last_title = nom[0]["title"]
                id = id +1
            nom[1] = id

    json.dump(json_input, outf)

def convert_hugo_1984_data_to_test_sets():
    """ Converts Hugo 1984 categorically sorted data into canonizer test and training data sets. """
    test_data = "TestData/txt_data/catsort.txt"
    convert_txt_to_json(test_data, "TestData/data.json")

    split_data("TestData/data.json", "TestData/training_data.json", "TestData/test_data.json", 0.1)
    convert_json_file_to_nomination_file("TestData/training_data.json", "TestData/training_nominations.json")
    pre_process_training_data("TestData/training_nominations.json", "TestData/training_nominations_classified.json")

def split_nominations(input_file, first_output, second_output, probability) :
    """ Splits a file line by line. Probability parameter determines the ratio of the split """
    first_file = open(first_output, "w")
    second_file = open(second_output, "w")
    original_data = open(input_file, "r")

    nominations = json.load(first_file);

    set1 = {"entries": []}
    set2 = {"entries": []}

    # TODO: Split the entries between two sets

    for line in original_data:
        rnd = random.random()
        if rnd < probability:
            first_file.writelines(line)
        else:
            second_file.writelines(line)

def convert_hugo_1984_data_to_test_sets2():
    """ Converts Hugo 1984 categorically sorted data into canonizer test and training data sets. """
    test_data = "TestData/txt_data/catsort.txt"
    convert_txt_to_json(test_data, "TestData/data.json")
    convert_json_file_to_nomination_file("TestData/data.json", "TestData/nominations.json")
    pre_process_training_data("TestData/nominations.json", "TestData/nominations_classified.json")

    split_nominations("TestData/nominations_classified.json", "TestData/training_data.json", "TestData/test_data.json", 0.1)


def run_tests():
    """ Early test run """
    train_file = open("TestData/training_nominations_classified.json", "r")

    # Tests
    c = classifier.HugoClassifier()

    s = train_file.read()

    c.train_json(s)

    test_file = open("TestData/test_data.json")

    for line in test_file:
        ent = json.loads(line)
        cat = ent['category']
        ent['category'] = category_encoding[int(cat) - 1]
        print ent['title']
        print c.canonize(ent)
