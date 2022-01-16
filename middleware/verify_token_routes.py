from fastapi import Request
from fastapi.routing import APIRoute
from funtions_jwt import validate_token


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            token = request.headers["Authorization"].split(" ")[1]
            validate_response = validate_token(token, output=False)

            if validate_response is None:
                return await original_route
            else:
                return validate_response

        return verify_token_middleware
