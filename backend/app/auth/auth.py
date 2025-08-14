from app.auth.utils.load_config import ALGORITHM, TOKEN_LEN
from passlib.context import CryptContext
from datetime import timedelta
import secrets

class AuthenticationTools:
    
    def __init__(self):
        self.bcrypt_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    def hash(self, plaintext : str) -> str:
        return self.bcrypt_context.hash(plaintext)
    
    def compare_hash(self, password : str, hashed_password : str) -> bool:
        return self.bcrypt_context.verify(password, hashed_password)
    
    def create_token(self):
        return secrets.token_hex(TOKEN_LEN) 
            