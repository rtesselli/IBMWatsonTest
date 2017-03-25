import os
import urllib
import zipfile
from collections import defaultdict
from string import split, strip

def removeFromString(string, strings_to_remove):
    for s in strings_to_remove:
        string = string.replace(s, "")
    return string

def URLDecorator(func, URL):
    def func_wrapper(text):
        return URL+func(text)
    return func_wrapper

def fileTypeDecorator(func, type):
    def func_wrapper(text):
        return func(text)+"."+type
    return func_wrapper

def loadCSV(file_name, all_classes, classes):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            try:
                elements = defaultdict(list)
                for line in f:
                    (image_id, image_class) = split(strip(line),',')
                    if all_classes or image_class in classes:
                        elements[image_class].append(image_id)
                return elements
            except:
                return None
    else:
        return None

def createZipCollections(collections, path, URL_decorator, file_decorator):
    total_imgs = 0
    for key in collections.keys():
        total_imgs += len(collections[key])
    counter = 0
    for key in collections.keys():
        if not os.path.exists(path):
            os.makedirs(path)
        with zipfile.ZipFile(path+key+".zip", 'w') as zip_file:
            for element in collections[key]:
                try:
                    print("Downloading: {0}, [{1:<2}%]".format(URL_decorator(element), (counter*100)/total_imgs))
                    local_file = urllib.urlretrieve(URL_decorator(element))
                    zip_file.write(local_file[0], file_decorator(element), zipfile.ZIP_DEFLATED)
                except:
                    print "Error while downloading " + URL_decorator(element)
                counter += 1
