from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from organization_manager.core.config import settings
from organization_manager.db.database import SessionLocal
from organization_manager.db.repos.user import UserRepository
from organization_manager.schemas.auth import LoginRequest, TokenResponse
from organization_manager.services.auth_service import AuthService

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repo(db_session=Depends(get_db)) -> UserRepository:
    return UserRepository(
        db_session=db_session
    )


def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    return AuthService(user_repo=user_repo)


# Login endpoint
@router.post("/login", response_model=TokenResponse)
async def login(login_req: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.authenticate_user(login_req.email, login_req.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth_service.create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )
