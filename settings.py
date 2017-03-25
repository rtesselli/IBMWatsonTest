import json

class Settings:
    def __init__(self, args):
        if args['settings'] is None:
            print("Loading default settings")
            self.api_key = raw_input("Please enter the api-key: ")
            self.api_version = '2016-05-20'
            self.training_size = 1
            self.classes = frozenset()
            self.all_classes = True
            self.classificator_id = None
            self.classificator_name = "ClassificatorV1"
            self.image_URL = "http://ypic.yoox.biz/ypic/yoox/-resize/180/f/"
            self.image_type = "jpg"
            self.data_file = "./training_set.csv"
        else:
            try:
                with open(args['settings'], "r") as f:
                    string = " ".join(f.readlines())
            except:
                raise IOError
            parsed_json = json.loads(string)
            self.api_key = parsed_json["api_key"]
            self.api_version = parsed_json["api_version"]
            self.training_size = parsed_json["training_size"]
            self.classes = frozenset(parsed_json["classes"])
            self.all_classes = parsed_json["all_classes"]
            self.classificator_id = parsed_json["classificator_id"]
            self.classificator_name = parsed_json["classificator_name"]
            self.image_URL = parsed_json["image_URL"]
            self.image_type = parsed_json["image_type"]
            self.data_file = parsed_json["data_file"]

    def __repr__(self):
        return "Settings()"

    def __str__(self):
        d = {
        "api_key" : self.api_key,
        "api_version" : self.api_version,
        "training_size" : self.training_size,
        "classes" : self.classes,
        "all_classes" : self.all_classes,
        "classificator_id" : self.classificator_id,
        "classificator_name" : self.classificator_name,
        "image_URL" : self.image_URL,
        "image_type" : self.image_type,
        "data_file" : self.data_file,
        }
        return str(d)
