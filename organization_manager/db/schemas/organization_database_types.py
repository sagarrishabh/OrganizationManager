from pydantic import BaseModel

from organization_manager.db.schemas.organization_types import OrganizationDomainModel


class CreateOrganizationDatabaseRequest(BaseModel):
    organization: OrganizationDomainModel

    @property
    def database_name(self):
        return f"{self.organization.id}_{self.organization.name}"

    @property
    def database_url(self):
        return f'sqlite:///{self.database_name}.db'

    class Config:
        orm_mode = True
        from_attributes = True


class OrganizationDatabaseDomainModel(BaseModel):
    id: int
    database_name: str
    database_url: str

    class Config:
        orm_mode = True
        from_attributes = True
