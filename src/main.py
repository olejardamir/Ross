from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routing import ApiRouter
from app.config.settings import settings


# see https://youtrack.jetbrains.com/issue/PY-76760/support-type-matching-ParamSpeced-Protocols-FASTAPI-CorsMiddleware-type-issue
def create_app() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )  # type: ignore
    fastapi_app.include_router(ApiRouter().router)
    return fastapi_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        ssl_keyfile=settings.SSL_KEYFILE,
        ssl_certfile=settings.SSL_CERTFILE,
    )