from app.endpoints.dependencies import get_current_user, get_session_id
from fastapi import Response, status

def test_get_session_id():
    
    header = "Bearer SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA"
    
    assert get_session_id(header) == "SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA"
    
def test_get_session_id_missing_token():
    
    header = "Bearer"
    
    response = get_session_id(header)
    
    assert isinstance(response, Response)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.body == b"Missing session id"
    
def test_get_session_id_invalid_token_type():
    
    header = "wrong-token"
    
    response = get_session_id(header)
    
    assert isinstance(response, Response)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.body == b"Invalid token type"
    
def test_get_current_user(session_service):
    
    token = "Bearer SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA"

    assert get_current_user(session_id=get_session_id(token), session_service=session_service) == 1 
    
    
def test_get_current_user_wrong_token(session_service):
    
    token = "Bearer wrong-token"

    response = get_current_user(session_id=get_session_id(token), session_service=session_service)

    assert isinstance(response, Response)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.body == b"session invalid"
    