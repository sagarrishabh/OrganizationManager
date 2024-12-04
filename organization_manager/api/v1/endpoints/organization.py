from fastapi import APIRouter, Depends, HTTPException

from organization_manager.db.database import SessionLocal
from organization_manager.db.repos.organization import OrganizationRepository
from organization_manager.schemas.organization import OrganizationCreate, OrganizationDomainModel
from organization_manager.services.create_database_service import CreateOrganizationDatabaseService
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


def get_create_organization_database_service() -> CreateOrganizationDatabaseService:
    return CreateOrganizationDatabaseService()


def get_organization_service(
        organization_repo: OrganizationRepository = Depends(get_organization_repo),
        create_organization_database_service: CreateOrganizationDatabaseService = Depends(
            get_create_organization_database_service)
) -> OrganizationService:
    return OrganizationService(
        organization_repo=organization_repo,
        create_organization_database_service=create_organization_database_service
    )


@router.post("/create", response_model=OrganizationDomainModel)
async def create_organization(
        org_create: OrganizationCreate,
        organization_service: OrganizationService = Depends(get_organization_service)
):
    try:
        return await organization_service.create_organization(org_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
