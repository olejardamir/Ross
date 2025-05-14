from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse

from Ross_git.src.app.services.status_service import StatusService


class ApiRouter:
    def __init__(self):
        self.router = APIRouter()
        self.status_service = StatusService()
        self.add_routes()

    def add_routes(self):
        self.router.add_api_route("/status", self.get_status, methods=["GET"])
        self.router.add_api_route("/echo", self.post_echo, methods=["POST"])

    async def get_status(self, request: Request):
        if request.url.scheme != "https":
            return JSONResponse(
                content={"error": "HTTPS required"},
                status_code=status.HTTP_403_FORBIDDEN
            )
        message = self.status_service.get_status()
        return {"message": message}

    async def post_echo(self, request: Request):
        if request.url.scheme != "https":
            return JSONResponse(
                content={"error": "HTTPS required"},
                status_code=status.HTTP_403_FORBIDDEN
            )
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON"
            )
        return {"received": body}
