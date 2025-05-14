from fastapi import APIRouter, Depends, Request, status, HTTPException

from Ross_git.src.app.controllers.echo_controller import EchoController
from Ross_git.src.app.controllers.status_controller import StatusController
from Ross_git.src.app.services.echo_service import EchoService
from Ross_git.src.app.services.status_service import StatusService

# Revised Dependency Injection Setup
def get_status_controller():
    return StatusController()

def get_status_service(
    controller: StatusController = Depends(get_status_controller)
) -> StatusService:
    return StatusService(controller)

def get_echo_controller():
    return EchoController()

def get_echo_service(
    controller: EchoController = Depends(get_echo_controller)
) -> EchoService:
    return EchoService(controller)

# Security Dependency
def https_required(request: Request):
    if request.url.scheme != "https":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="HTTPS required"
        )

# Route Handlers with Improved DI
async def post_echo(
    request: Request,
    _: None = Depends(https_required),  # Security check first
    echo_service: EchoService = Depends(get_echo_service),
):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON"
        )

    message = echo_service.handle_echo(body)
    return {"message": message}

async def get_status(
    _: None = Depends(https_required),  # Security check first
    status_service: StatusService = Depends(get_status_service),
):
    message = status_service.get_status()
    return {"message": message}

# Router Class
class ApiRouter:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):
        self.router.add_api_route("/status", get_status, methods=["GET"])
        self.router.add_api_route("/echo", post_echo, methods=["POST"])