from models.utils.load_env import URL
from models.utils.auth import TokenAuth
import requests
from  requests import Response
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
     

class UserModel():
    def __init__(self):
        self.url = URL

    def get_user(self):
        
        response = requests.get(url=f"{self.url}/user/profile", auth=TokenAuth())
        
        logger.debug(f"get user data {response.json()}")
        
        return response