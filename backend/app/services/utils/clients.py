### CLIENT RESPONSIBLE FOR CONNECTING TO COMPUTING SERVER ###
import logging
import requests
from typing import List, Union

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ComputeClient:
    
    def __init__(self, base_url : str):
        self.base_url = base_url
    
    
    def send_request(self, data : List[List[float]]
                     ) -> Union[List[List[int]], List[int]]:

        payload : dict = {
            "data" : data
        }
        
        response = requests.post(f"{self.base_url}/models/lr", json=payload)

        
        logger.debug(f"Received compute data {response.json()}")
            
        response.raise_for_status()
        
        return response.json()
        
        