from sqlalchemy import create_engine

from organization_manager.db.models.base import OrganizationBase
from organization_manager.db.repos.organization_database_repo import OrganizationDatabaseRepository
from organization_manager.db.schemas.organization_database_types import CreateOrganizationDatabaseRequest, \
    OrganizationDatabaseDomainModel
from organization_manager.utils.custom_logger import CustomLogger

logger = CustomLogger().get_logger()


class OrganizationDatabaseService:
    def __init__(self, organization_database_repo: OrganizationDatabaseRepository):
        self.organization_database_repo = organization_database_repo

        logger.info("OrganizationDatabaseService Initialized")

    async def create_organization_database(
            self,
            create_organization_database_request: CreateOrganizationDatabaseRequest
    ) -> OrganizationDatabaseDomainModel:
        logger.info(
            f"OrganizationDatabaseService.create_organization_database called with database_url: {create_organization_database_request.database_url}",
            extra={
                "database_url": create_organization_database_request.database_url,
                "organization_id": create_organization_database_request.organization.id,
            })

        # Create organization database
        engine = create_engine(create_organization_database_request.database_url)
        OrganizationBase.metadata.create_all(engine)

        logger.info("Organization database created successfully")

        # Save organization database record to master db
        organization_database = await self.organization_database_repo.create_database_record(
            create_organization_database_request=create_organization_database_request)

        logger.info("Organization database record created successfully")

        return organization_database
