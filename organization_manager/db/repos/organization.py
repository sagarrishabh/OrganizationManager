from sqlalchemy.orm import Session

from organization_manager.db.models.organization import Organization
from organization_manager.schemas.organization import OrganizationCreate, OrganizationDomainModel


class OrganizationRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, org_create: OrganizationCreate) -> OrganizationDomainModel:
        organization = Organization(
            email=str(org_create.email),
            organization_name=org_create.organization_name
        )

        self.db_session.add(organization)
        self.db_session.commit()
        self.db_session.refresh(organization)

        return OrganizationDomainModel.from_orm(organization)
