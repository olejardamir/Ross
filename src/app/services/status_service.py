from Ross_git.src.app.controllers.status_controller import StatusController

class StatusService:
    def __init__(self, controller: StatusController):
        self.controller = controller

    def get_status(self) -> str:
        return self.controller.check_status()
