from pydantic import BaseModel, EmailStr


class OrganizationCreateRequest(BaseModel):
    email: EmailStr
    password: str
    organization_name: str


class GetOrganizationRequest(BaseModel):
    organization_name: str
    offset: int = 0,
    limit: int = 10


class OrganizationDomainModel(BaseModel):
    id: int
    organization_name: str

    class Config:
        orm_mode = True
        from_attributes = True
