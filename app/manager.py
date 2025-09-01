import logging
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
    
    def load_data(self):
        """ 

        """
        data = self.__loader.load_csv(config.DATA)
        self.__elastic.connect()
        self.__elastic.create_index(config.ES_INDEX, config.MAPPING)
        self.__elastic.index_documents(config.ES_INDEX, data)

    def process(self):
        """
        
        """
        self.__elastic.connect()
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

        """
        query = {"query": {
                    "bool": {
                        "must": [
                            { "match": { "Antisemitic": "0" }},
                            { "terms": { "Sentiment": ["neutral", "positive"] }}],
                        "must_not": [
                            { "exists": { "field": "Weapons" }}]}}}
        self.__elastic.delete_documents(config.ES_INDEX, query)

    def run(self):
        """
        """
        logging.info("Starting process the data...")
        self.process()
        self.delete()
        self.__is_processed = True
        logging.info("Data processing completed")
    
    @property
    def status(self):
        """ 
        """
        return self.__is_processed
