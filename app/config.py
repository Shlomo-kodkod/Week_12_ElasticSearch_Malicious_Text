import os


BLACK_LIST = "data/weapon_list.txt"
DATA = "data/tweets_injected 3.csv"

ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_INDEX = os.getenv("ES_INDEX", "iranian_data")
MAPPING = {
    "properties": {
        "TweetID": {"type": "text"},
        "CreateDate": {"type": "text"},
        "Antisemitic": {"type": "text"},
        "Text": {"type": "text"},
        "Sentiment": {"type": "text"},
        "Weapons": {"type": "text"}
    }
}


