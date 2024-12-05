from typing import List

from organization_manager.db.repos.organization_repo import OrganizationRepository
from organization_manager.db.repos.user_repo import UserRepository
from organization_manager.db.schemas.organization_types import OrganizationDomainModel, OrganizationGetRequest, \
    OrganizationCreateRequest
from organization_manager.db.schemas.user_types import OrganizationUserCreateRequest
from organization_manager.services.dynamic_database_service import OrganizationDatabaseService


class OrganizationService:
    def __init__(self,
                 organization_repo: OrganizationRepository,
                 user_repo: UserRepository,
                 organization_database_service: OrganizationDatabaseService
                 ):
        self.organization_repo = organization_repo
        self.create_organization_database_service = organization_database_service
        self.user_repo = user_repo

    async def get_organization_by_name(self, org_get_request: OrganizationGetRequest) -> List[OrganizationDomainModel]:
        organizations = await self.organization_repo.get_organization_by_name(org_get_request)
        return organizations

    async def create_organization(self, org_create: OrganizationCreateRequest) -> OrganizationDomainModel:
        organization = await self.organization_repo.create_organization(org_create)
        organization_user = await self.user_repo.create_organization_user(org_user_create=OrganizationUserCreateRequest(
            organization_id=organization.id,
            email=org_create.email,
            password=str(org_create.password)
        ))

        return organization
