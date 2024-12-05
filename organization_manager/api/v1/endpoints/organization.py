from typing import List

from fastapi import APIRouter, Depends, HTTPException

from organization_manager.db.database import SessionLocal
from organization_manager.db.repos.organization_database_repo import OrganizationDatabaseRepository
from organization_manager.db.repos.organization_repo import OrganizationRepository
from organization_manager.db.repos.user_repo import UserRepository
from organization_manager.db.schemas.dynamic_database_types import CreateOrganizationDatabaseRequest
from organization_manager.db.schemas.organization_types import OrganizationDomainModel, OrganizationCreateRequest, \
    GetOrganizationRequest
from organization_manager.db.schemas.user_types import OrganizationUserCreateRequest
from organization_manager.services.dynamic_database_service import OrganizationDatabaseService
from organization_manager.services.organization_admin_service import OrganizationAdminService
from organization_manager.services.organization_service import OrganizationService

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_organization_repo(db_session=Depends(get_db)) -> OrganizationRepository:
    return OrganizationRepository(db_session=db_session)


def get_user_repo(db_session=Depends(get_db)) -> UserRepository:
    return UserRepository(
        db_session=db_session
    )


def get_organization_service(
        organization_repo: OrganizationRepository = Depends(get_organization_repo),
) -> OrganizationService:
    return OrganizationService(
        organization_repo=organization_repo,
    )


def get_organization_database_repo(db_session=Depends(get_db)) -> OrganizationDatabaseRepository:
    return OrganizationDatabaseRepository(db_session=db_session)


def get_organization_database_service(
        organization_database_repo: OrganizationDatabaseRepository = Depends(
            get_organization_database_repo)
) -> OrganizationDatabaseService:
    return OrganizationDatabaseService(organization_database_repo=organization_database_repo)


def get_organization_admin_service(user_repo: UserRepository = Depends(get_user_repo)
                                   ) -> OrganizationAdminService:
    return OrganizationAdminService(user_repo=user_repo)


@router.post("/create", response_model=OrganizationDomainModel)
async def create_organization(
        org_create: OrganizationCreateRequest,
        organization_service: OrganizationService = Depends(get_organization_service),
        organization_database_service: OrganizationDatabaseService = Depends(get_organization_database_service),
        organization_admin_service: OrganizationAdminService = Depends(get_organization_admin_service)
):
    try:
        organization = await organization_service.create_organization(org_create)
        organization_database = await organization_database_service.create_organization_database(
            create_organization_database_request=CreateOrganizationDatabaseRequest(
                organization=organization
            )
        )
        organization_admin = await organization_admin_service.create_organization_user(
            org_user_create=OrganizationUserCreateRequest(
                email=org_create.email,
                password=org_create.password,
                organization_id=organization.id
            )
        )

        return OrganizationDomainModel.from_orm(
            organization
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get", response_model=List[OrganizationDomainModel])
async def get_organization(
        org_get_request: GetOrganizationRequest = Depends(),
        organization_service: OrganizationService = Depends(get_organization_service)
):
    try:
        return await organization_service.get_organization_by_name(org_get_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
