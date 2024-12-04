from organization_manager.db.repos.organization import OrganizationRepository
from organization_manager.db.repos.user import UserRepository
from organization_manager.schemas.organization import OrganizationCreateRequest, OrganizationDomainModel
from organization_manager.schemas.organization_database import OrganizationDBCreateRequest
from organization_manager.schemas.user import OrganizationUserCreateRequest
from organization_manager.services.create_database_service import CreateOrganizationDatabaseService


class OrganizationService:
    def __init__(self,
                 organization_repo: OrganizationRepository,
                 user_repo: UserRepository,
                 create_organization_database_service: CreateOrganizationDatabaseService
                 ):
        self.organization_repo = organization_repo
        self.create_organization_database_service = create_organization_database_service
        self.user_repo = user_repo

    async def create_organization(self, org_create: OrganizationCreateRequest) -> OrganizationDomainModel:
        organization = await self.organization_repo.create(org_create)
        organization_user = await self.user_repo.create_organization_user(org_user_create=OrganizationUserCreateRequest(
            organization_id=organization.id,
            email=org_create.email,
            password=str(org_create.password)
        ))

        self.create_organization_database_service.create_database(organization=organization)

        return organization
