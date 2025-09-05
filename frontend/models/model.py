import abc
from models.utils.load_env import URL
from app_state import AppState
from models.utils.auth import TokenAuth

class Model(abc.ABC):
    
    def __init__(self):
        self.url = URL
        self.session_id = AppState().session_id
        self.token_auth = TokenAuth(self.session_id)