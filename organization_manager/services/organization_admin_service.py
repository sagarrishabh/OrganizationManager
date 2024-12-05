from organization_manager.db.repos.user_repo import UserRepository
from organization_manager.db.schemas.user_types import OrganizationUserCreateRequest, OrganizationUserDomainModel
from organization_manager.utils.custom_logger import CustomLogger

logger = CustomLogger().get_logger()


class OrganizationAdminService:
    def __init__(self, user_repo: UserRepository, ):
        self.user_repo = user_repo
        logger.info("OrganizationAdminService Initialized")

    async def create_organization_user(
            self,
            org_user_create: OrganizationUserCreateRequest
    ) -> OrganizationUserDomainModel:
        logger.info(
            f"OrganizationAdminService.create_organization_user called for {org_user_create.email} and organization_id: {org_user_create.organization_id}",
            extra={
                "email": org_user_create.email,
                "organization_id": org_user_create.organization_id,
            })
        # Create organization user
        organization_user = await self.user_repo.create_organization_user(org_user_create=org_user_create)

        logger.info("Organization user created successfully", extra={
            "organization_user_id": organization_user.id,
            "organization_id": organization_user.organization.id,
        })

        return organization_user
