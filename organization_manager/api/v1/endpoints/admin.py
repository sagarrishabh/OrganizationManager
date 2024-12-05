from datetime import timedelta
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from organization_manager.core.config import settings
from organization_manager.db.database import get_db
from organization_manager.db.repos.user_repo import UserRepository
from organization_manager.db.schemas.auth_types import LoginRequest, TokenResponse
from organization_manager.exceptions import UserGetError
from organization_manager.services.auth_service import AuthService
from organization_manager.utils.custom_logger import CustomLogger

logger = CustomLogger().get_logger()
router = APIRouter()


def get_user_repo(db_session=Depends(get_db)) -> UserRepository:
    return UserRepository(
        db_session=db_session
    )


def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    return AuthService(user_repo=user_repo)


# Login endpoint
@router.post("/login", response_model=TokenResponse)
async def login(login_req: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    logger.info(f"API called to login for email: {login_req.email}", extra={
        "email": login_req.email,
    })

    try:
        user = await auth_service.authenticate_user(login_req.email, login_req.password)
        if not user:
            logger.error("Incorrect username or password")
            raise UserGetError("Incorrect username or password")

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await auth_service.create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        return TokenResponse(
            access_token=access_token,
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
