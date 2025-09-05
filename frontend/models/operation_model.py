import requests
import logging
from models.model import Model

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class OperationModel(Model):
    
    def get_operations(self):
        response = requests.get(f"{self.url}/operations/data", auth=self.token_auth)
        logger.debug(f"fetched data :{response.json()}")
        
        return response.json()
        