from pydantic import BaseModel


class OrganizationDBCreateRequest(BaseModel):
    id: int
    organization_name: str

    class Config:
        orm_mode = True
        from_attributes = True
