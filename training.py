import sys
import os
import argparse
import random
import json
import settings as s
import utilities as u
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import WatsonException

def parseArguments():
    """
    Defines the arguments used by the main program
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--settings", type=str, help="specify settings file")
    return arg_parser.parse_args()

def getRandomTrainingSet(collection, num_elem):
    """
    Returns a random subset of size num_elem from collection
    """
    assert(num_elem < len(collection))
    already_picked = set()
    max_id = len(collection) - 1
    training_set = []
    for i in xrange(num_elem):
        new_index = random.randint(0, max_id)
        while new_index in already_picked:
            new_index = random.randint(0, max_id)
        assert new_index not in already_picked
        already_picked.add(new_index)
        training_set.append(collection[new_index])
    return training_set

def createRandomTrainingSets(elements, training_size):
    """
    Returns a random training set for each class in elements
    """
    training_sets = dict()
    for image_class in elements.keys():
        training_sets[image_class] = getRandomTrainingSet(elements[image_class], training_size)
    return training_sets

def trainWatson(api_version, api_key, path, classificator_name):
    """
    Loads all the .zip files in the path folder and calls the API to train IBM Watson
    with the loaded .zip files
    """
    if not os.path.exists(path):
        sys.exit("Image directory does not exist, exiting program")
    else:
        visual_recognition = VisualRecognitionV3(version = api_version, api_key = api_key)
        files = []
        zipfiles = [f for f in os.listdir(path) if ".zip" in f]
        args = dict()
        args['name'] = classificator_name
        result = None
        for filename in zipfiles:
            try:
                files.append(open(path+filename, 'r'))
                filename = u.removeFromString(filename, [".zip", "-", "\\", "|", "*", "{", "}", "$", "/", "'","`", "\""])
                args[filename+"_positive_examples"] = files[len(files) - 1]
            except:
                for f in files:
                    f.close()
                sys.exit("Something went wrong while loading ZIP file, exiting program")
        try:
            result = visual_recognition.create_classifier(**args)
        except WatsonException, e:
            for f in files:
                f.close()
            print(e)
            sys.exit("Something went wrong while creating classifier")
        for f in files:
            f.close()
        return result

if __name__ == "__main__":
    """
    This program has all the workflow necessary to train a new IBM Watson visual create_classifier
    from scratch.
    It parse the arguments and loads the program settings accordingly.
    Then it process the CSV file with the image IDs and classes and creates the
    random training sets for each class specified in the settings.
    Once the training sets are ready it downloads the images from the web and
    stores them in .zip files inside the subdirectory "./images/".
    When the .zip files are ready it calls the IBM API to create and train the
    visual classificator.
    """
    arguments = parseArguments()
    try:
        settings = s.Settings(vars(arguments))
    except:
        sys.exit("Something went wrong while loading settings, exiting program")
    elements = u.loadCSV(settings.data_file, settings.all_classes, settings.classes)
    if elements is None or not elements:
        sys.exit("Something went wrong while loading CSV file, exiting program")
    training_sets = createRandomTrainingSets(elements, settings.training_size)
    file_decorator = u.fileTypeDecorator(lambda x : x, settings.image_type)
    URL_decorator = u.URLDecorator(file_decorator, settings.image_URL)
    u.createZipCollections(training_sets, settings.image_dir, URL_decorator, file_decorator)
    trainWatson(settings.api_version, settings.api_key, settings.image_dir, settings.classificator_name)
    print(json.dumps(trainWatson(settings.api_version, settings.api_key, settings.image_dir, settings.classificator_name), indent = 2))
