import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging


class Processor:
    @staticmethod
    def calculate_sentiment_score(text: str) -> str:
        """
        Analyzes the sentiment of a given text string and returns a sentiment score.
        """
        score= SentimentIntensityAnalyzer().polarity_scores(text)
        result = score["compound"]
        logging.info("Successfully calculated sentiment score")
        if result >= 0.5: return "positive"
        elif result <= -0.5: return "negative"
        else: return "neutral"

    
    @staticmethod
    def find_weapons(text: str, weapons: list) -> list | None:
        """
        Find weapons in the given text using the provided set of weapons.
        """
        found_weapons = [weapon for weapon in weapons if weapon in text]
        if found_weapons:
            logging.info("Successfully found weapons")
            return found_weapons
        else:
            logging.info("Weapons not found")
            return None
    
        

    

        
    

    