from pydantic import BaseModel, EmailStr


class OrganizationCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str


class OrganizationDomainModel(BaseModel):
    id: int
    email: EmailStr
    organization_name: str

    class Config:
        orm_mode = True
        from_attributes = True
