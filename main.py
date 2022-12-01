from fastapi import FastAPI
from src.api.routes.v1 import user_routes
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

app.include_router(user_routes.router)

# @app.get("/")
# def root():
#     return {"message": "Hello World"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

import datetime

print(datetime.datetime.now())