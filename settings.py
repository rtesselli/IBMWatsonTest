class Settings:
    def __init__(self, args):
        if args['settings'] is None:
            print("Loading default settings")
            #self.api_key = raw_input("Please enter the api-key: ")
            self.api_key = 'f41e2b93981dbafab11eefb99a125e5f84993eec' #TODO rimetti raw_input
            self.api_version = '2016-05-20'
            self.training_size = 1
            self.classes = frozenset()
            self.all_classes = True
            self.classificator_id = "ClassificatorV1"
            self.image_URL = "http://ypic.yoox.biz/ypic/yoox/-resize/180/f/"
            self.image_type = "jpg"
            self.data_file = "./training_set.csv"
        else:
            print("TODO load and parse settings file")
