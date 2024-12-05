from pydantic import BaseModel, EmailStr, Field


class OrganizationCreateRequest(BaseModel):
    """
    Represents a request to create a new organization with necessary details.

    This class is used for creating a request to add a new organization to the system.
    It contains user identification through email and password, and the name of the
    organization to be created.

    Attributes:
        email: EmailStr
            Email of the user.
        password: str
            Password of the user.
        organization_name: str
            Name of the organization.
    """
    email: EmailStr = Field(description="Email of the user", examples=["abc@example.com"])
    password: str = Field(description="Password of the user", examples=["qwerty1234567890"])
    organization_name: str = Field(description="Name of the organization", examples=["Nava"])


class GetOrganizationRequest(BaseModel):
    organization_name: str
    offset: int = 0,
    limit: int = 10


class OrganizationDomainModel(BaseModel):
    id: int = Field(description="Id of the organization", examples=[1234])
    name: str = Field(description="Name of the organization", examples=["Nava"])

    class Config:
        orm_mode = True
        from_attributes = True
