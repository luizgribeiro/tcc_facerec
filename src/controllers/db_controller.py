import logging 
import pymongo
from configs.db_configs import db_configs
logging.basicConfig(level=logging.INFO)

class DataBase():

    def __init__(self):
        logging.info("Setting up database connection")
        try:
            self.client = pymongo.MongoClient(db_configs['db_uri'])
            self.db = self.client.face_recog_atendence
        except:
            raise Exception("Unable to connect to database")
        else:
            logging.info("Database connection stablished")

    def __del__(self):
        self.client.close()