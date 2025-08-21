from app.auth.auth import AuthenticationTools
from datetime import datetime, timedelta
from app.services.utils.load_config import SESSION_DURATION
import socket
from app.services.utils.unit import UnitOfWorkSession
from app.services.exceptions import SessionExpiredError, SessionNotFoundError
from datetime import datetime
from app.database.models import UserSession

class SessionService:
    
    def __init__(self, auth_tools : AuthenticationTools, session_uow : UnitOfWorkSession):
        self.auth_tools = auth_tools
        self.session_uow = session_uow
        
    def create_session(self, user_id : int) -> str:
        
        created_at : datetime = datetime.now()
        expires_at : datetime = created_at + timedelta(seconds=SESSION_DURATION if SESSION_DURATION else 3600)
        metadata : dict[str, str] = {
            "ip" : socket.gethostbyname(socket.gethostname()),
            "device" : "desktop"
        }
        
        session_id : str = self.auth_tools.create_session_id()
        
        with self.session_uow as uow:
            uow.repository.save_session(
                session_id=session_id,
                user_id=user_id,
                created_at=created_at,
                expires_at=expires_at,
                last_active=created_at,
                roles=["User"],
                metadata=metadata
            )
            
            uow.commit()
            
        return session_id

    def get_current_user(self, session_id : str) -> int:
        
        with self.session_uow as uow:
            session : UserSession = uow.repository.get_session(session_id=session_id)
            
            if session is None:
                raise SessionNotFoundError

            if session.expires_at < datetime.now():
                raise SessionExpiredError
            
            return session.user_id
    
    def delete_session(self, user_id : int) -> None:
        
        with self.session_uow as uow:
            uow.repository.delete_session(user_id=user_id)

            uow.commit()