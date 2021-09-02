from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.api.api_v1.api import api_router
from app.core import config
from app.db.session import session
from app.core.jwt import validate_token, reusable_oauth2

app = FastAPI(
    title=config.PROJECT_NAME, openapi_url=config.API_ROOT_PATH + "/openapi.json"
)

origins = [
    "http://localhost",
    "null"
]  # yapf: disable

origin_regex = "http://localhost:[0-9]+"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=config.API_ROOT_PATH)


@app.middleware("http")
async def token_validate_middleware(request: Request, call_next):

    allow_no_authenticate = [
        config.API_ROOT_PATH + "/login/access-token",
        config.API_ROOT_PATH + '/users/create_user',
        "/docs",
        "/api/v1/openapi.json"
    ]  # yapf: disable

    if request.url.path not in allow_no_authenticate:
        print("validate token..........")
        token = await reusable_oauth2(request)
        current_user = validate_token(request.state.db, token)
        request.state.user = current_user

    print("Correct token! ")

    response = await call_next(request)
    return response


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response: Response = Response("Internal server error", status_code=500)
    try:
        request.state.db = session()
        print("get DB session")
        response = await call_next(request)

    finally:
        request.state.db.close()
        print("close DB session")
    return response


if __name__ == "__main__":
    print("\n\n============================================================")
    for name, value in vars(config).items():
        if name[:2] != "__":
            print('%s=%s' % (name, value))
    print("============================================================\n\n")
    pass
