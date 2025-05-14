from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routing import ApiRouter  # Ensure this path is correct
from app.config.settings import settings  # Load settings from .env


def create_app() -> FastAPI:
    app = FastAPI()

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(ApiRouter().router)

    return app


# Expose FastAPI app for Uvicorn
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
