from sqlalchemy import create_engine

from organization_manager.db.models.base import OrganizationBase
from organization_manager.db.repos.organization_database_repo import OrganizationDatabaseRepository
from organization_manager.db.schemas.dynamic_database_types import CreateOrganizationDatabaseRequest, \
    OrganizationDatabaseDomainModel


class OrganizationDatabaseService:
    def __init__(self, organization_database_repo: OrganizationDatabaseRepository):
        self.organization_database_repo = organization_database_repo

    async def create_organization_database(
            self,
            create_organization_database_request: CreateOrganizationDatabaseRequest
    ) -> OrganizationDatabaseDomainModel:
        engine = create_engine(create_organization_database_request.database_url)
        OrganizationBase.metadata.create_all(engine)

        organization_database = await self.organization_database_repo.create_database_record(
            create_organization_database_request=create_organization_database_request)

        return organization_database
