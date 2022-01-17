from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    descrip: str

    class Config:
        orm_mode = True


class UserReadSchema(BaseModel):
    id: int
    name: str
    descrip: str

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: Optional[str]
    descrip: Optional[str]

    class Config:
        orm_mode = True


class UserAuthenticaSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
