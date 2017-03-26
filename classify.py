import sys
import argparse
import settings as s
import utilities as u
import json
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import WatsonException

def parseArguments():
    """
    Defines the arguments used by the main program
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--settings", type=str, help="specify settings file")
    arg_parser.add_argument("image_id", help="specify image id or .txt file with multiple ids")
    return arg_parser.parse_args()

def classify(URL_decorator, threshold, classificator_id, image_id):
    """
    Classify an image given its id by using a given IBM Watson visual classificator.
    It returns a string with the classification result
    """
    try:
        result =visual_recognition.classify(images_url=URL_decorator(image_id), threshold=0.1, classifier_ids=[classificator_id])
    except:
        return None
    for i in xrange(result["images_processed"]):
        if not "error" in result["images"][i]:
            (bestscore, bestclass) = (0, None)
            for cl in result["images"][i]["classifiers"][0]["classes"]:
                if cl["score"] > bestscore:
                    (bestscore, bestclass) = (cl["score"], cl["class"])
            return str("image {0} is {1} with score {2}".format(result["images"][i]["resolved_url"], bestclass, bestscore))
        return None


if __name__ == "__main__":
    """
    This programs checks if the classificator is ready-to-use.
    If so it proceeds to classify all the images given in input with the settings provided
    """
    arguments = parseArguments()
    try:
        settings = s.Settings(vars(arguments))
    except:
        sys.exit("Something went wrong while loading settings, exiting program")
    if settings.classificator_id is None:
        settings.classificator_id = raw_input("Insert classificator ID: ")

    visual_recognition = VisualRecognitionV3(version = settings.api_version, api_key = settings.api_key)
    try:
        result = visual_recognition.get_classifier(settings.classificator_id)
    except:
        sys.exit("Cannot reach the classifier, exiting program")
    if result["status"] == "ready":
        image_id = vars(arguments)["image_id"]
        file_decorator = u.fileTypeDecorator(lambda x : x, settings.image_type)
        URL_decorator = u.URLDecorator(file_decorator, settings.image_URL)
        if ".txt" in image_id:
            try:
                images_id = open(image_id, "r").read().split()
            except:
                sys.exit("Something went wrong while loading input file, exiting program")
            for image_id in images_id:
                result = classify(URL_decorator,0.1,settings.classificator_id, image_id)
                if result is None:
                    print("Error while calling the classificator on image "+ image_id)
                else:
                    print(result)
        else:
            result = classify(URL_decorator,0.1,settings.classificator_id, image_id)
            if result is None:
                print("Error while calling the classificator on image "+ image_id)
            else:
                print(result)
