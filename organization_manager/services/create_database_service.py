from sqlalchemy import create_engine

from organization_manager.db.models.base import OrganizationBase
from organization_manager.schemas.organization import OrganizationDomainModel


class CreateOrganizationDatabaseService:
    def __init__(self):
        pass

    def create_database(self, organization: OrganizationDomainModel) -> bool:
        database_url = f'sqlite:///{organization.id}_{organization.organization_name}.db'
        engine = create_engine(database_url)
        OrganizationBase.metadata.create_all(engine)

        return True
