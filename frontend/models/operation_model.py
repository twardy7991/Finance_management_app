from models.utils.load_env import URL
import requests
from models.utils.auth import TokenAuth
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class OperationModel:
    
    def __init__(self):
        self.url = URL
    
    def get_operations(self):
        response = requests.get(f"{self.url}/operations/data", auth=TokenAuth())
        logger.debug(f"fetched data :{response.json()}")
        
        return response.json()
        