from organization_manager.db.repos.organization import OrganizationRepository
from organization_manager.schemas.organization import OrganizationCreate, OrganizationDomainModel
from organization_manager.services.create_database_service import CreateOrganizationDatabaseService


class OrganizationService:
    def __init__(self,
                 organization_repo: OrganizationRepository,
                 create_organization_database_service: CreateOrganizationDatabaseService
                 ):
        self.organization_repo = organization_repo
        self.create_organization_database_service = create_organization_database_service

    async def create_organization(self, org_create: OrganizationCreate) -> OrganizationDomainModel:
        # Create organization database:
        self.create_organization_database_service.create_database(organization_name=org_create.organization_name)

        return await self.organization_repo.create(org_create)
