import logging
import copy
from app.loader import Loader
from app.elastic import Elastic
from app.processor import Processor
from app import config

class Manager:
    def __init__(self):
        self.__loader = Loader()
        self.__elastic = Elastic()
        self.__processor = Processor()
        self.__blacklist = self.__loader.load_txt(config.BLACK_LIST)
        self.__is_processed = False
        self.__elastic.connect()
    
    def load_data(self):
        """ 
        Load data from CSV file and create elasticsearch index.
        """
        data = self.__loader.load_csv(config.DATA)
        self.__elastic.create_index(config.ES_INDEX, config.MAPPING)
        self.__elastic.index_documents(config.ES_INDEX, data)

    def process(self):
        """
        Processes existing data in the elasticsearch index:
        """
        data = self.__elastic.search(config.ES_INDEX)
        new_data = list()
        for doc in data:
            original_data = doc['_source']
            new_data.append(
                {"id": doc["_id"], "data": 
                {"Sentiment": self.__processor.calculate_sentiment_score(original_data["text"]),
                "Weapons": self.__processor.find_weapons(original_data["text"], self.__blacklist)}})
        self.__elastic.update_documents(config.ES_INDEX, new_data)

    def delete(self):
        """
        Deletes not antisemitic with neutral or positive sentiment and without weapons documents from the index.
        """
        query = config.DELETE_QUERY
        self.__elastic.delete_documents(config.ES_INDEX, query)

    def run(self):
        """
        Execute the data processing.
        """
        logging.info("Starting process the data...")
        self.load_data()
        self.process()
        self.delete()
        self.__is_processed = True
        logging.info("Data processing completed")
    
    def search_by_weapons(self, weapons_cnt):
        """
        Searches for antisemitic documents by number of weapons.
        """
        query = copy.deepcopy(config.BASE_API_QUERY)
        query["query"]["bool"]["must"][2]["script"]["script"]["params"]["min_weapons"] = weapons_cnt

        result = self.__elastic.search(config.ES_INDEX, query)
        return result



    
    @property
    def status(self):
        """ 
        Return the data processing status.
        """
        return self.__is_processed
