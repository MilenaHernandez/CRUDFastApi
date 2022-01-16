from fastapi import  APIRouter
from pydantic import BaseModel, EmailStr
from funtions_jwt import write_token
from fastapi.responses import JSONResponse

auth_routes = APIRouter()

class User(BaseModel):
    email: EmailStr
    password: str

@auth_routes.post("/login")
def login(user: User):
    print(user.dict())
    """Aqui debe hacerce la validacion contra la base de datos 
    de usuarios registrados, ejemplo quemado"""
    if user.email == "mhernandez@correo.com" and user.password == "1234":
        return write_token(user.dict())
    else:
        return JSONResponse(content={"message": "Usuario no valido"}, status_code=404)
