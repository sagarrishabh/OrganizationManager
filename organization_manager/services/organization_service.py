from typing import List

from organization_manager.db.repos.organization_repo import OrganizationRepository
from organization_manager.db.schemas.organization_types import OrganizationDomainModel, GetOrganizationRequest, \
    OrganizationCreateRequest
from organization_manager.utils.custom_logger import CustomLogger

logger = CustomLogger().get_logger()


class OrganizationService:
    def __init__(self, organization_repo: OrganizationRepository):
        self.organization_repo = organization_repo

        logger.info("OrganizationService Initialized")

    async def get_organization_by_name(self, org_get_request: GetOrganizationRequest) -> List[OrganizationDomainModel]:
        organizations = await self.organization_repo.get_organization_by_name(org_get_request)
        return organizations

    async def create_organization(self, org_create_request: OrganizationCreateRequest) -> OrganizationDomainModel:
        logger.info(
            f"OrganizationService.create_organization called with organization_name: {org_create_request.organization_name} and email: {org_create_request.email}",
            extra={
                "email": org_create_request.email,
                "organization_name": org_create_request.organization_name,
            })

        organization = await self.organization_repo.create_organization(org_create_request=org_create_request)

        logger.info("Organization created successfully", extra={
            "organization_id": organization.id,
            "organization_name": organization.name,
        })

        return organization
