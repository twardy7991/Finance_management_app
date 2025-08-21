import pytest

from app.services import SessionService
from app.services.exceptions import SessionNotFoundError

def test_get_current_user(session_service : SessionService):
    
    session_id = 'SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA'
    
    assert session_service.get_current_user(session_id=session_id) == 1
    
def test_create_session(session_service : SessionService):
    
    user_id = 2
    
    session_id = session_service.create_session(user_id=user_id)
    
    assert session_service.get_current_user(session_id=session_id) == 2
    
def test_delete_session(session_service : SessionService):
    
    session_id = 'SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA'
    user_id = 1
    
    session_service.delete_session(user_id=user_id)
    
    with pytest.raises(SessionNotFoundError):
        session_service.get_current_user(session_id=session_id)