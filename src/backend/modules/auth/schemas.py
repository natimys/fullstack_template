from pydantic import BaseModel, EmailStr, SecretStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr


class UserLogin(BaseModel):
    username: str
    password: SecretStr


class UserPublic(BaseModel):
    username: str
    email: EmailStr
