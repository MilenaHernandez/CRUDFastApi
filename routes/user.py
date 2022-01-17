from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.db import conn, engine
from middleware.verify_token_routes import VerifyTokenRoute
from models import user_model
from models.user_model import UserModel
from schemas.user_schema import UserCreateSchema, UserUpdateSchema, UserReadSchema

user = APIRouter(route_class=VerifyTokenRoute)
user_model.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = conn()
        yield db
    finally:
        db.close()


@user.get("/", response_model=List[UserReadSchema])
def get_users(db: Session = Depends(get_db)):
    usuarios = db.query(UserModel).all()
    return usuarios


@user.get("/{user_id}", response_model=UserReadSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UserModel).get(user_id)
    if usuario is None:
        return JSONResponse(content={"message": "Usuario no existe"}, status_code=200)
    return usuario


@user.post("/", response_model=UserCreateSchema)
def create_user(nuevo: UserCreateSchema, db: Session = Depends(get_db)):
    usuario = UserModel(email=nuevo.email,
                        password=nuevo.password,
                        name=nuevo.name,
                        descrip=nuevo.descrip)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@user.put("/{user_id}", response_model=UserCreateSchema)
def update_user(user_id: int, update: UserUpdateSchema, db: Session = Depends(get_db)):
    usuario = db.query(UserModel).filter_by(id=user_id).first()
    if usuario is None:
        return JSONResponse(content={"message": "Usuario no existe"}, status_code=200)
    else:
        try:
            usuario.name = update.name
            usuario.descrip = update.descrip
            db.commit()
            db.refresh(usuario)
        except Exception:
            db.rollback()
            return JSONResponse(content={"message": "Error interno del servidor"}, status_code=500)
    return usuario


@user.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UserModel).filter_by(id=user_id).first()
    if usuario is None:
        return JSONResponse(content={"message": "Usuario no existe"}, status_code=200)
    else:
        try:
            db.delete(usuario)
            db.commit()
        except Exception:
            db.rollback()
            return JSONResponse(content={"message": "Error interno del servidor"}, status_code=500)
        return JSONResponse(content={"message": "Usuario eliminado"}, status_code=200)
