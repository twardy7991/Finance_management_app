from passlib.context import CryptContext
from app.auth.utils.load_config import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from app.containers import Container
from dependency_injector.providers import Provider



class AuthenticationTools:
    
    def __init__(self):
            
        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecrated='auto')

    def hash(self, plaintext : str) -> str:
        return self.bcrypt_context.hash(plaintext)
    
    def compare_hash(self, password : str, hashed_password : str) -> bool:
        return self.bcrypt_context.verify(password, hashed_password)
    
    def create_access_token(self, username : str, user_id : int, expires_delta : timedelta):
        
        encode = {'sub' : username, 'id' : user_id}
        expires = datetime.now() + expires_delta
        encode.update({'exp' : expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def check_token(
        token : str
    ):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')

        return username, user_id
            