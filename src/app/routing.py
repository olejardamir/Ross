from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse

class ApiRouter:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):
        """Define and add routes to the router."""
        self.router.add_api_route("/status", self.get_status, methods=["GET"])
        self.router.add_api_route("/echo", self.post_echo, methods=["POST"])

    async def get_status(self, request: Request):
        """Handle GET requests to /status."""
        if request.url.scheme != "https":
            return JSONResponse(
                content={"error": "HTTPS required"},
                status_code=status.HTTP_403_FORBIDDEN
            )
        return {"message": "Service is up"}

    async def post_echo(self, request: Request):
        """Handle POST requests to /echo."""
        if request.url.scheme != "https":
            return JSONResponse(
                content={"error": "HTTPS required"},
                status_code=status.HTTP_403_FORBIDDEN
            )

        try:
            body = await request.json()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON"
            )

        return {"received": body}
