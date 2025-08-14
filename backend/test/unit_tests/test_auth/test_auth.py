import pytest
from app.auth.auth import AuthenticationTools
from passlib.hash import sha256_crypt

@pytest.fixture
def auth_tools():
    auth_tools = AuthenticationTools()
    return auth_tools

def test_hash(auth_tools : AuthenticationTools):
    
    plaintext = "password" 
    ciphertext = auth_tools.hash(plaintext)
    
    assert sha256_crypt.verify(plaintext, ciphertext)
    
def test_compare_hash(auth_tools : AuthenticationTools):
    
    plaintext = "password" 
    ciphertext = sha256_crypt.hash(plaintext)
    
    assert auth_tools.compare_hash(plaintext, ciphertext)