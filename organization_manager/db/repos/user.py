from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from organization_manager.db.models.user import User, OrganizationUserMapping
from organization_manager.exceptions import OrganizationUserCreationError
from organization_manager.schemas.user import OrganizationUserCreateRequest, OrganizationUserDomainModel, \
    UserDomainModel, AuthUserDomainModel
from organization_manager.utils.hash_password import hash_password


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, org_user_create) -> UserDomainModel:
        user = User(
            email=str(org_user_create.email),
            hashed_password=hash_password(org_user_create.password),
        )
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)

        return UserDomainModel.from_orm(user)

    async def create_organization_user(
            self,
            org_user_create: OrganizationUserCreateRequest
    ) -> OrganizationUserDomainModel:
        try:
            user = await self.create_user(org_user_create)

            organization_user_mapping = OrganizationUserMapping(
                organization_id=org_user_create.organization_id,
                user_id=user.id,
            )

            self.db_session.add(organization_user_mapping)
            self.db_session.commit()
            self.db_session.refresh(organization_user_mapping)

            return OrganizationUserDomainModel.from_orm(organization_user_mapping)

        except SQLAlchemyError as e:
            self.db_session.rollback()

            # Handle exception as needed, such as logging
            raise OrganizationUserCreationError from e

    async def get_auth_user(self, email: EmailStr) -> AuthUserDomainModel:
        user = self.db_session.query(User).filter(User.email == email).first()
        return AuthUserDomainModel.from_orm(user)
