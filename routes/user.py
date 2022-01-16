from dotenv.cli import get
from fastapi import APIRouter
from pydantic import BaseModel
from middleware.verify_token_routes import VerifyTokenRoute

user = APIRouter(route_class=VerifyTokenRoute)


class User (BaseModel):
    name: str
    description: str


@user.post("/users")
def users(args):
    return get(f'peticion a DB')