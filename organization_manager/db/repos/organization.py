from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from organization_manager.db.models.organization import Organization
from organization_manager.exceptions import OrganizationCreationError
from organization_manager.schemas.organization import OrganizationCreateRequest, OrganizationDomainModel


class OrganizationRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, org_create: OrganizationCreateRequest) -> OrganizationDomainModel:
        try:
            organization = Organization(
                organization_name=org_create.organization_name
            )

            self.db_session.add(organization)
            self.db_session.commit()
            self.db_session.refresh(organization)

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise OrganizationCreationError

        return OrganizationDomainModel.from_orm(organization)
