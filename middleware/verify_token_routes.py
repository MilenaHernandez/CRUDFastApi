from fastapi import Request
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse

from funtions_jwt import validate_token


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            try:
                token = request.headers["Authorization"].split(" ")[1]
                validate_response = validate_token(token, output=False)

                if validate_response is None:
                    return await original_route(request)
                else:
                    return validate_response
            except Exception:
                return JSONResponse(content={"message": "Sin autorizacion"}, status_code=200)

        return verify_token_middleware