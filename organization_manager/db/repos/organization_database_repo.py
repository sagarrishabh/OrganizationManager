from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from organization_manager.db.models.organization import OrganizationDatabase
from organization_manager.db.schemas.organization_database_types import OrganizationDatabaseDomainModel, \
    CreateOrganizationDatabaseRequest
from organization_manager.exceptions import OrganizationDatabaseCreationError
from organization_manager.utils.custom_logger import CustomLogger

logger = CustomLogger().get_logger()


class OrganizationDatabaseRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

        logger.info("OrganizationDatabaseRepository Initialized")

    async def create_database_record(
            self, create_organization_database_request: CreateOrganizationDatabaseRequest
    ) -> OrganizationDatabaseDomainModel:
        logger.info(
            f"OrganizationDatabaseRepository.create_database_record called with database_name: {create_organization_database_request.database_name} and organization_id: {create_organization_database_request.organization.id} and database_url: {create_organization_database_request.database_url}",
            extra={
                "database_name": create_organization_database_request.database_name,
                "organization_id": create_organization_database_request.organization.id,
                "database_url": create_organization_database_request.database_url,
            })

        try:
            organization_database = OrganizationDatabase(
                organization_id=create_organization_database_request.organization.id,
                database_name=create_organization_database_request.database_name,
                database_url=create_organization_database_request.database_url,
            )

            self.db_session.add(organization_database)
            self.db_session.commit()
            self.db_session.refresh(organization_database)

        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(" Error while creating organization database DB entry", exc_info=e, extra={
                "database_name": create_organization_database_request.database_name,
            })
            raise OrganizationDatabaseCreationError

        return OrganizationDatabaseDomainModel.from_orm(organization_database)
