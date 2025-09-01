from elasticsearch import Elasticsearch , helpers
import logging
from app import config

class Elastic:
    def __init__(self):
        self.__uri = f"http://{config.ES_HOST}:{config.ES_PORT}"
        self.__connection = None 

    def connect(self):
        """
        Connect to elasticsearch server.
        """
        try:
            self.__connection = Elasticsearch([self.__uri], verify_certs=True)
            if self.__connection.ping():
                logging.info("Successfully connected to Elasticsearch")
            else:
                logging.error("Failed to connect to Elasticsearch")
        except Exception as e:
            logging.error(f"Failed to connect to elastic {e}")
            raise e

    def create_index(self, index_name: str, map: dict):
        """
        Creates a new index in elasticsearch if it doesn't exist.
        """
        if not self.__connection.indices.exists(index=index_name):
            self.__connection.indices.create(index=index_name, mappings=map)
            logging.info(f"Successfully create index {index_name}")
        else:
            logging.warning(f"Index {index_name} already exists")
            
        
    def index_documents(self, index_name: str, data: list):
        """
        Indexing documents into elasticsearch.
        """
        try:
            actions = [{"_index": index_name, "_source": doc} for doc in data]
            helpers.bulk(client=self.__connection, actions=actions)
            logging.info(f"Successfully indexed documents")
        except Exception as e:
            logging.error(f"Failed to index data: {e}")
            raise e
        
        
    def update_documents(self, index_name: str, data: dict):
        """
        Updates existing documents in elasticsearch.
        """
        try:
            actions = [{"_op_type": "update","_index": index_name,"_id": doc.get("id", None),"doc": doc.get("data", None)} for doc in data]
            helpers.bulk(client=self.__connection, actions=actions)
            logging.info(f"Successfully update documents")
        except Exception as e:
            logging.error(f"Failed to update documents: {e}")
            raise e
        
    def delete_documents(self, index_name: str, query: dict):
        """
        Deletes documents from index based on query.
        """
        try:
            response = self.__connection.delete_by_query(index=index_name, body=query)
            if response.get('deleted', 0) > 0:
                logging.info(f"Documents successfully deleted")
            else:
                logging.info("Documents to delete not found")
        except Exception as e:
            logging.error(f"Failed to delete documents: {e}")
            raise e
        
    def search(self, index_name: str, query: dict = {"query": {"match_all": {}}}, score: bool = False) -> list:
        """
        Searches for documents in elasticsearch index.
        """
        try:
            result = helpers.scan(client=self.__connection, index=index_name, query=query)
            docs = [document for document in result] if not score else [document["_source"] for document in result]
            logging.info(f"Successfully search {query}")
            return docs 
        except Exception as e:
            logging.error(f"Failed to search {query}: {e}")
            raise e
            
                         


    