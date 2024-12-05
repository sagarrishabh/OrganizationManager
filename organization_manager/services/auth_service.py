from datetime import timedelta, datetime
from typing import Optional

import jwt
from pydantic import EmailStr

from organization_manager.core.config import settings
from organization_manager.db.repos.user_repo import UserRepository
from organization_manager.db.schemas.user_types import UserDomainModel
from organization_manager.utils.custom_logger import CustomLogger
from organization_manager.utils.hash_password import verify_password

logger = CustomLogger().get_logger()


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        logger.info("AuthService Initialized")

    async def authenticate_user(self, email: EmailStr, password: str) -> Optional[UserDomainModel]:
        logger.info(f"AuthService.authenticate_user called for email: {email}", extra={
            "email": email,
        })
        auth_user = await self.user_repo.get_auth_user(email=email)
        if verify_password(password, auth_user.hashed_password):
            logger.info("User authenticated successfully")
            return UserDomainModel(**auth_user.dict())

        logger.error("Incorrect username or password")
        return None

    # Create the JWT token
    async def create_access_token(self, data: dict, expires_delta: timedelta = 15):
        logger.info("AuthService.create_access_token called")

        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt
