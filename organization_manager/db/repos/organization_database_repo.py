from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from organization_manager.db.models.organization import OrganizationDatabase
from organization_manager.db.schemas.dynamic_database_types import OrganizationDatabaseDomainModel, \
    CreateOrganizationDatabaseRequest
from organization_manager.exceptions import OrganizationCreationError, OrganizationDatabaseCreationError


class OrganizationDatabaseRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_database_record(
            self, create_organization_database_request: CreateOrganizationDatabaseRequest
    ) -> OrganizationDatabaseDomainModel:
        try:
            organization_database = OrganizationDatabase(
                organization_id=create_organization_database_request.organization_id,
                database_name=create_organization_database_request.database_name,
                database_url=create_organization_database_request.database_url,
            )

            self.db_session.add(organization_database)
            self.db_session.commit()
            self.db_session.refresh(organization_database)

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise OrganizationDatabaseCreationError

        return OrganizationDatabaseDomainModel.from_orm(organization_database)
