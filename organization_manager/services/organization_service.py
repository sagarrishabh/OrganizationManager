from typing import List

from organization_manager.db.repos.organization_repo import OrganizationRepository
from organization_manager.db.schemas.organization_types import OrganizationDomainModel, GetOrganizationRequest, \
    OrganizationCreateRequest


class OrganizationService:
    def __init__(self, organization_repo: OrganizationRepository):
        self.organization_repo = organization_repo

    async def get_organization_by_name(self, org_get_request: GetOrganizationRequest) -> List[OrganizationDomainModel]:
        organizations = await self.organization_repo.get_organization_by_name(org_get_request)
        return organizations

    async def create_organization(self, org_create: OrganizationCreateRequest) -> OrganizationDomainModel:
        organization = await self.organization_repo.create_organization(org_create)

        return organization
