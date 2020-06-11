import logging 
from pymodm import connect

from .configs.db_configs import db_configs
logging.basicConfig(level=logging.INFO)

class DataBase():

    def __init__(self, database_name):
        logging.info("Setting up database connection")
        try:
            #self.client = 
            connect(f'{db_configs["db_URI"]}{database_name}')
        except:
            raise Exception("Unable to connect to database")
        else:
            logging.info("Database connection stablished")
