from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from organization_manager.db.models.organization import Organization
from organization_manager.exceptions import OrganizationCreationError, OrganizationGetError
from organization_manager.schemas.organization import OrganizationCreateRequest, OrganizationDomainModel, \
    OrganizationGetRequest


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

    async def get_by_name(
            self,
            org_get_request: OrganizationGetRequest,

    ) -> List[OrganizationDomainModel]:
        try:
            query = (
                self.db_session.query(Organization)
                .filter(Organization.organization_name.like(f"%{org_get_request.organization_name}%"))
                .offset(org_get_request.offset)
                .limit(org_get_request.limit)
            )

            organizations = query.all()
            if not organizations:
                raise OrganizationGetError("No organizations found")

            # Convert ORM objects to domain models
            return [OrganizationDomainModel.from_orm(org) for org in organizations]

        except SQLAlchemyError as e:
            raise OrganizationGetError from e
