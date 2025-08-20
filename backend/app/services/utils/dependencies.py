from fastapi import Header, Response, status, Depends
from dependency_injector.wiring import Provide, inject

from app.containers import Container
from app.services import SessionService
from app.services.exceptions import SessionExpiredError, SessionNotFoundError

async def get_session_id(authorization : str = Header(...)):
    scheme, _, session_id = authorization.partition(" ")
    
    if scheme.lower() != "bearer" or not session_id:
        raise Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Invalid or missing session id",
        )

    return session_id

@inject
async def check_session(session_id : str = Depends(get_session_id),
                         session_service : SessionService = Depends(Provide[Container.session_service])):
    try:
        session_service.get_current_user(session_id=session_id)
    except SessionNotFoundError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND,
                        content=str(e))
    except SessionExpiredError as e:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED,
            content=str(e)
        )
    
    return session_id