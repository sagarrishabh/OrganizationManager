from pydantic import BaseModel, EmailStr

from organization_manager.schemas.organization import OrganizationDomainModel


class OrganizationUserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    organization_id: int


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
