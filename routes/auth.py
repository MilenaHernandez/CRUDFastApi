from fastapi import APIRouter, Header
from fastapi.params import Depends
from sqlalchemy.orm import Session

from config.db import engine, conn
from funtions_jwt import write_token, validate_token
from fastapi.responses import JSONResponse

from models import user_model
from models.user_model import UserModel
from schemas.user_schema import UserAuthenticaSchema

auth_routes = APIRouter()
user_model.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = conn()
        yield db
    finally:
        db.close()


@auth_routes.post("/login")
def login(userAuthen: UserAuthenticaSchema, db: Session = Depends(get_db)):
    print(userAuthen.dict())
    user = db.query(UserModel).filter_by(email=userAuthen.email, password=userAuthen.password).first()
    if user is None:
        return JSONResponse(content={"message": "Usuario no valido"}, status_code=404)
    else:
        return write_token(userAuthen.dict())


@auth_routes.post("/verify/token")
def verify_token(Authorized: str = Header(None)):
    token = Authorized.split(" ")[1]
    return validate_token(token, output=True)


@auth_routes.post("/register")
def register(newUser: UserAuthenticaSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(email=newUser.email).first()
    if user is None:
        if user.password.equal(newUser.password):
            user = UserModel(email=newUser.email,
                             password=newUser.password)
            db.add(user)
            db.commit()
            db.refresh(user)
            return JSONResponse(content={"message": "Usuario registrado" + newUser.dict()}, status_code=200)
        else:
            return JSONResponse(content={"message": "Contraseña incorrecta"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Usuario ya existe"}, status_code=200)
