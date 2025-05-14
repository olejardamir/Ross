# src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routing import ApiRouter  # Ensure this path is correct


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

    # Run directly (no need to reference "src.main" when calling from this file)
    uvicorn.run(
        "main:app",  # NOT "src.main:app" when running from inside `src/`
        host="127.0.0.1",
        port=8000,
        reload=True,
        ssl_keyfile="./app/config/key.pem",
        ssl_certfile="./app/config/cert.pem"
    )
