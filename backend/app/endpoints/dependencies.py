from fastapi import Header, Response, status, Depends
from dependency_injector.wiring import Provide, inject

from fastapi import HTTPException
from app.database.models import UserSession
from app.containers import Container
from app.services import SessionService
from app.services.exceptions import SessionExpiredError, SessionNotFoundError

def get_session_id(authorization : str = Header(...)):
    scheme, _, session_id = authorization.partition(" ")
    
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
        
    if not session_id:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing session id",
        )

    return session_id

@inject
def get_current_user(session_id : str = Depends(get_session_id),
                    session_service : SessionService = Depends(Provide[Container.session_service])):
    try:
        user_id : UserSession = session_service.get_current_user(session_id=session_id)
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e))
    except SessionExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
    return user_id