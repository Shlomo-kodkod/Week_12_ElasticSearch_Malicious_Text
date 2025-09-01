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
        "text": {"type": "text"},
        "Sentiment": {"type": "text"},
        "Weapons": {"type": "keyword"
        }
    }
}

DELETE_QUERY = {
        "query": {
             "bool": {
                 "must": [
                     { "match": { "Antisemitic": "0" }},
                     { "terms": { "Sentiment": ["neutral", "positive"] }}],
                "must_not": [
                    { "exists": { "field": "Weapons" }}]}}}


BASE_API_QUERY = {
    "query": {
        "bool": {
            "must": [
                {"match": {"Antisemitic": "1"}},
                {"exists": {"field": "Weapons"}},
                {"script": {
                    "script": {
                        "source": "doc['Weapons'].length >= params.min_weapons",  
                        "lang": "painless",
                        "params": {
                            "min_weapons": 0}}}}],
            "must_not": [
                {"term": {"Weapons": "none"}}]}}}