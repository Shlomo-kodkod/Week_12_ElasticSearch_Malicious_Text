from csv import DictReader
import logging


class Loader:
    @staticmethod
    def load_csv(file_path: str) -> dict:
        "Load data from csv and return dictionary."
        try:
            with open("geeks.csv", 'r') as file:
                dict_reader = DictReader(file)
            logging.info("Data loaded successfully")
            return dict_reader
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
            raise e
    
    @staticmethod
    def load_txt(file_path: str) -> list:   
        """
        Load a blacklist of weapons from data and return list of weapons.
        """
        try:
            with open(file_path, 'r') as file:
                blacklist = list(file.read().splitlines())
            logging.info("Blacklist loaded successfully.")
            return blacklist
        except Exception as e:
            logging.error(f"Failed to load blacklist: {e}")
            raise e

                