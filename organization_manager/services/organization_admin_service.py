from organization_manager.db.repos.user_repo import UserRepository
from organization_manager.db.schemas.user_types import OrganizationUserCreateRequest, OrganizationUserDomainModel


class OrganizationAdminService:
    def __init__(self, user_repo: UserRepository, ):
        self.user_repo = user_repo

    async def create_organization_user(
            self,
            org_user_create: OrganizationUserCreateRequest
    ) -> OrganizationUserDomainModel:
        organization_user = await self.user_repo.create_organization_user(org_user_create=org_user_create)

        return organization_user
