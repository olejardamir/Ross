from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routing import ApiRouter  # Make sure this exists and works


class RossApp:
    def __init__(self):
        self.app = FastAPI()
        self.setup_cors()
        self.include_routers()

    def setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def include_routers(self):
        self.app.include_router(ApiRouter().router)

    def get_app(self) -> FastAPI:
        return self.app


# This is the actual FastAPI app exposed to Uvicorn
app = RossApp().get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",  # Make sure this points to the correct module:var path
        host="127.0.0.1",
        port=8000,
        reload=True,
        ssl_keyfile="./app/config/key.pem",
        ssl_certfile="./app/config/cert.pem"
    )
