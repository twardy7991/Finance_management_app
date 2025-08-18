from passlib.hash import sha256_crypt

from app.services.user_service import UserService
from app.services.authentication_service import AuthenticationService
from app.database.models import User, Credential


def test_get_user(user_service :  UserService):
    user_id = 2
    
    saved_user = User(
        user_id = user_id,
        name = "Jane",
        surname = "Smith", 
        telephone = "987654321",
        address = "456 Elm St, Springfield"
    )
    
    assert saved_user.is_equal(user_service.get_user(user_id=user_id))

def test_register_user(user_service : UserService, authentication_service : AuthenticationService):
    
    username = "Josee"
    password = "Inverio"
    name = "Name"
    surname = "Surname"
    telephone = "123456789"
    address = "Rakowicka 6/52 Catania"
    
    user_id = user_service.register_user(
        username=username,
        password=password,
        name=name,
        surname=surname,
        telephone=telephone,
        address=address
    )
    
    saved_user = User(
        name = name,
        surname = surname,
        telephone = telephone,
        address = address
    )
    
    saved_credentials = Credential(
        user_id = user_id,
        username = username,
        password = password
    )
    
    assert saved_user.is_equal(user_service.get_user(user_id=user_id))
    
    credential_in_db = authentication_service.get_credential(username=username)
    
    assert credential_in_db.is_equal(saved_credentials, sha256_crypt)
    

        