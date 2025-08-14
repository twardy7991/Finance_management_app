

from app.database.repositories import CredentialRepository
from app.auth.auth import AuthenticationTools
from app.database.models import Credential


# def test_get_credentials(credential_repository : CredentialRepository):
    
#     username = 'janesmith'
#     saved_credentials = Credential(
#         user_id = 2,
#         username = username,
#         password = 'pass2'
#     )
    
#     assert saved_credentials.is_equal(credential_repository.get_credentials(username=username)) 
    
# def test_save_credentials(credential_repository : CredentialRepository, user_repository):
    
#     user_id = user_repository.save_user(name="Jose",
#                               surname="Inverio",
#                               telephone="500338659",
#                               address="Racławicka 6/52")
    
#     auth = AuthenticationTools()
    
#     username = "username123"
#     password = "password123"
#     hashed_password = auth.hash(password)
    
#     credential_repository.save_credentials(user_id=user_id,
#                                            username=username,
#                                            hashed_password=hashed_password)
    
#     saved_credential = Credential(
#         user_id = user_id,
#         username = username,
#         password = hashed_password
#     )
    
#     assert saved_credential.is_equal(credential_repository.get_credentials(username=username))
    
    