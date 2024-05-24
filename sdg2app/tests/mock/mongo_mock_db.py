from bson.json_util import loads
import mongomock
from os.path import abspath, join, dirname


class MongoMockDB():
    def __init__(self) -> None:
        self.db = mongomock.MongoClient().db
        self.data = {}  # store raw data from files
        self.collection_name_list = [
            "users", "folders", "scenarios", "tasks", "jobs"
        ]
        self.load_data()

    def load_data(self):
        # load data from data files
        for collection_name in self.collection_name_list:
            with open(
                    join(join(abspath(dirname(__file__)), "data"),
                         "{}.json".format(collection_name))) as f:
                file_data = loads(f.read())
            collection = self.db[collection_name]
            collection.insert_many(file_data)
            self.data[collection_name] = file_data

    def clear_data(self):
        # clear db data
        for collection_name in self.collection_name_list:
            self.db[collection_name].drop()

    def reset(self):
        self.clear_data()
        self.load_data()
