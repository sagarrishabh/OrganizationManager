from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from organization_manager.db.models.organization import Organization
from organization_manager.db.schemas.organization_types import OrganizationCreateRequest, OrganizationDomainModel, \
    GetOrganizationRequest
from organization_manager.exceptions import OrganizationCreationError, OrganizationGetError
from organization_manager.utils.custom_logger import CustomLogger

logger = CustomLogger().get_logger()

class OrganizationRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

        logger.info("OrganizationRepository Initialized")

    async def create_organization(self, org_create_request: OrganizationCreateRequest) -> OrganizationDomainModel:
        logger.info(f"OrganizationRepository.create_organization called with organization_name: {org_create_request.organization_name}", extra={
            "organization_name": org_create_request.organization_name,
        })

        try:
            organization = Organization(
                organization_name=org_create_request.organization_name
            )

            self.db_session.add(organization)
            self.db_session.commit()
            self.db_session.refresh(organization)

        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(" Error while creating organization DB entry", exc_info=e, extra={
                "organization_name": org_create_request.organization_name,
            })
            raise OrganizationCreationError

        return OrganizationDomainModel.from_orm(organization)

    async def get_organization_by_name(
            self,
            org_get_request: GetOrganizationRequest,

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
