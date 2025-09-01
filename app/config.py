import os


BLACK_LIST = "data/weapon_list.txt"
DATA = "data/tweets_injected 3.csv"

ES_HOST = os.getenv("ES_HOST", "elastic")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_INDEX = os.getenv("ES_INDEX", "iranian_data")
MAPPING = {
            "mappings": {
                "properties": {
                    "title": {
                        "TweetID": "text",
                        "CreateDate": "text",
                        "Antisemitic": "text",
                        "Text": "text",
                        "Sentiment": "text",
                        "Weapons": "text" 
                    }
                }
            }
        }



