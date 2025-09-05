import requests
from  requests import Response
import logging
from models.model import Model

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
     
class UserModel(Model):
    
    def get_user(self):
        
        response = requests.get(url=f"{self.url}/user/profile", auth=self.token_auth)
        
        logger.debug(f"get user data {response.json()}")
        
        return response

    def update_user(self, data) -> bool:
        
        logger.debug(f"update user data : {data}")
        
        response = requests.patch(url=f"{self.url}/user/update", auth=self.token_auth, json=data)
        
        logger.debug(f"updated user data with response : {response.text}, status_code : {response.status_code}")
        
        if response.status_code == 200:
            return True
        return False