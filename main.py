from fastapi import FastAPI
from dotenv import load_dotenv
from routes.auth import auth_routes


app = FastAPI()
app.include_router(auth_routes, prefix="/api")
load_dotenv()

