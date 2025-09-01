from elasticsearch import Elasticsearch , helpers
import logging
from app import config

class Elastic:
    def __init__(self):
        self.__uri = f"http://{config.ES_HOST}:{config.ES_PORT}"
        self.__connection = None 

    def connect(self):
        try:
            self.__connection = Elasticsearch([self.__uri], verify_certs=True)
            if self.__connection.ping():
                logging.info("Successfully connected to Elasticsearch")
            else:
                logging.error("Failed to connect to Elasticsearch")
        except Exception as e:
            logging.error(f"Failed to connect to elastic {e}")
            raise(e)

    def create_index(self, index_name: str, map: dict):
        if not self.__connection.indices.exists(index=index_name):
            self.__connection.indices.create(index=index_name, mappings=map)
            logging.info(f"Successfully create index {index_name}")
        else:
            logging.warning(f"Index {index_name} already exists")
            
        
    def index_document(self, index_name: str, id: str, data: dict):
        try:
            self.__connection.index(index=index_name, id=id, body=data)
            logging.info(f"Successfully indexed document")
        except Exception as e:
            logging.error(f"Failed to index data: {e}")
            raise(e)
        
    def index_documents(self, index_name: str, action: list):
        try:
            helpers.bulk(client=self.__connection, actions=action)
            logging.info(f"Successfully indexed documents")
        except Exception as e:
            logging.error(f"Failed to index data: {e}")
            raise(e)
        
    def update_documents(self, index_name: str, id: str, data: dict):
        try:
            self.__connection.update(index=index_name, id=id, body=data)
            logging.info(f"Successfully update document {id}")
        except Exception as e:
            logging.error(f"Failed to update document {id}: {e}")
            raise(e)
        
    def delete_document(self, index_name: str, id: str):
        try:
            self.__connection.delete(index=index_name, id=id)
            logging.info(F"Successfully deleted documents {id}")
        except Exception as e:
            logging.error(f"Failed to delete document {id}")
            raise(e)
        
    def search(self, index_name: str, query: dict = {"match_all": {}}) -> list:
        try:
            result = self.__connection.search(index=index_name, body=query)
            docs = result['hits']['hits']
            logging.info(f"Successfully search {query}")
            return docs 
        except Exception as e:
            logging.error(f"Failed to search {query}: {e}")
            raise(e)
            
                         


    