from datetime import datetime
from app.database.repositories import SessionRepository
from app.database.models import UserSession

def test_get_session(session_repository : SessionRepository):
    
    user_session = UserSession(
        session_id='SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA',
        user_id=1,
        created_at=datetime(year=2025, month=8, day=20),
        expires_at=datetime(year=2025, month=12, day=30),
        last_active=datetime(year=2025, month=8, day=20),
    )

    assert user_session.is_equal(session_repository.get_session(session_id='SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA'))
    

def test_save_session(session_repository : SessionRepository):
    
    session_id = "session_id"
    user_id = 2
    created_at = datetime(year=2025, month=1, day=2, hour=10, minute=0, second=0)
    expires_at = datetime(year=2025, month=12, day=30, hour=10, minute=0, second=0)
    last_active = datetime(year=2025, month=1, day=2, hour=10, minute=0, second=0)
    roles = ["admin"]
    metadata = {"ip" : "127.0.0.0"}
    
    session_repository.save_session(session_id=session_id,
                                    user_id=user_id,
                                    created_at=created_at,
                                    expires_at=expires_at,
                                    last_active=last_active,
                                    roles=roles,
                                    metadata=metadata
                                    )
    
    user_session = UserSession(
        session_id=session_id,
         user_id=user_id,
        created_at=created_at,
        expires_at=expires_at,
        last_active=last_active,
        roles=roles,
        session_metadata=metadata
    )
    
    print(user_session)
    
    assert user_session.is_equal(session_repository.get_session(session_id=session_id))


def test_delete_session(session_repository : SessionRepository):
    
    session_repository.delete_session(user_id=1)
    
    assert session_repository.get_session(session_id='SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA') == None
