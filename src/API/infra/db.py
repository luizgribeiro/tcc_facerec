import logging 
from pymodm import connect
logging.basicConfig(level=logging.INFO)

class DataBase():

    def __init__(self, env_config):
        logging.info("Setting up database connection")
        try:
            db_url = self.uri_from_config(env_config)
            connect(db_url)
        except Exception as e:
            raise Exception(f"Unable to connect to database: {e}")
        else:
            logging.info("Database connection stablished")


    def uri_from_config(self, env_config):
        usr = env_config["MONGO_INITDB_ROOT_USERNAME"]
        pwd = env_config["MONGO_INITDB_ROOT_PASSWORD"]
        host = env_config["MONGO_HOST"]
        port = env_config["MONGO_PORT"]
        return f'mongodb://{usr}:{pwd}@{host}:{port}/face_rec?authSource=admin'





