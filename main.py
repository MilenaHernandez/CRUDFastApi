from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.responses import RedirectResponse

from routes.auth import auth_routes
from routes.user import user

app = FastAPI()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


app.include_router(auth_routes, prefix="/api")
app.include_router(user, prefix="/api/users")
load_dotenv()
