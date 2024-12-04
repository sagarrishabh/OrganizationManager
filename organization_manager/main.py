import uvicorn
from fastapi import FastAPI

from organization_manager.api.v1.endpoints import organization

app = FastAPI()

app.include_router(organization.router, prefix="/org", tags=["organizations"])
# app.include_router(admin.router, prefix="/admin", tags=["admin"])


if __name__ == "__main__":
    uvicorn.run("humanizer.app:app", host="127.0.0.1", port=8000, reload=False)
