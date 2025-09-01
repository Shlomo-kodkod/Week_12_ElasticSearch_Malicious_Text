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
            
        
    # def index_document(self, index_name: str, id: str, data: dict):
    #     try:
    #         self.__connection.index(index=index_name, id=id, body=data)
    #         logging.info(f"Successfully indexed document")
    #     except Exception as e:
    #         logging.error(f"Failed to index data: {e}")
    #         raise(e)
        
    def index_documents(self, index_name: str, data: list):
        try:
            actions = [{"_index": index_name, "_source": doc} for doc in data]
            helpers.bulk(client=self.__connection, actions=actions)
            logging.info(f"Successfully indexed documents")
        except Exception as e:
            logging.error(f"Failed to index data: {e}")
            raise(e)
        
    # def update_document(self, index_name: str, id: str, data: dict):
    #     try:
    #         self.__connection.update(index=index_name, id=id, body=data)
    #         logging.info(f"Successfully update document {id}")
    #     except Exception as e:
    #         logging.error(f"Failed to update document {id}: {e}")
    #         raise(e)
        
    def update_documents(self, index_name: str, data: dict):
        try:
            actions = [{"_op_type": "update","_index": index_name,"_id": doc.get("id", None),"doc": doc} for doc in data]
            helpers.bulk(client=self.__connection, actions=actions)
            logging.info(f"Successfully update documents")
        except Exception as e:
            logging.error(f"Failed to update documents: {e}")
            raise(e)
        
    def delete_documents(self, index_name: str, ids: list):
        try:
            actions = [{"_op_type": "delete","_index": index_name,"_id": id} for id in ids]
            helpers.bulk(client=self.__connection, actions=actions)
            logging.info(F"Successfully deleted documents")
        except Exception as e:
            logging.error(f"Failed to delete documents: {e}")
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
            
                         


    