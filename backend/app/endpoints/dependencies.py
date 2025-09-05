from fastapi import Header, Response, status, Depends
from dependency_injector.wiring import Provide, inject

from fastapi import HTTPException
from app.database.models import UserSession
from app.containers import Container
from app.services import SessionService
from app.services.exceptions import SessionExpiredError, SessionNotFoundError

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_session_id(authorization : str = Header(...)):
    scheme, _, session_id = authorization.partition(" ")
    
    if scheme.lower() != "bearer":
        logging.debug("Invalid token type")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
        
    if not session_id:
        logging.debug("Missing session id")
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
        logging.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e))
    except SessionExpiredError as e:
        logging.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
    logging.debug(f"fetched user_id : {user_id} from session")
    return user_id