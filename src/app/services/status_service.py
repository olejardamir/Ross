from Ross_git.src.app.controllers.status_controller import StatusController


class StatusService:
    def __init__(self, controller: StatusController = None):
        self.controller = controller or StatusController()

    def get_status(self) -> str:
        return self.controller.get_status_message()
