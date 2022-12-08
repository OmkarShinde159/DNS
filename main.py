from fastapi import FastAPI
from src.api.routes.v1 import login_auth_routes, signup_route,logout_route
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

app.include_router(signup_route.router)
app.include_router(login_auth_routes.router)
app.include_router(logout_route.router)

import datetime

print(datetime.datetime.now())