from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(description="Email of the user", examples=["abc@example.com"])
    password: str = Field(description="Password of the user", examples=["qwerty1234567890"])


class TokenResponse(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(description="JWT token type", default="bearer")
