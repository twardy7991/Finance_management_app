from requests.auth import AuthBase
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

TOKEN = ""

def set_token(token):
    TOKEN = token
    logger.debug(f"setting up token {token}")

class TokenAuth(AuthBase):
    
    def __init__(self, token = 'SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA'):
        if TOKEN != "":
            self.token = TOKEN
        else:
            self.token = token
            
        logger.debug(f"creating token: Bearer {token}")

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request