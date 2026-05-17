from pydantic import BaseModel, EmailStr, SecretStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr


class UserLogin(BaseModel):
    name: str
    password: SecretStr


class UserPublic(BaseModel):
    name: str
    email: EmailStr
