from pydantic import BaseModel, EmailStr

from organization_manager.db.schemas.organization_types import OrganizationDomainModel


class OrganizationUserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    organization_id: int


class AuthUserDomainModel(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserDomainModel(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
        from_attributes = True


class OrganizationUserDomainModel(BaseModel):
    id: int
    user: UserDomainModel
    organization: OrganizationDomainModel

    class Config:
        orm_mode = True
        from_attributes = True
