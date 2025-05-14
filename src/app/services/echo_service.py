from Ross_git.src.app.controllers.echo_controller import EchoController

class EchoService:
    def __init__(self, controller: EchoController):
        self.controller = controller

    def handle_echo(self, body: dict) -> str:
        return self.controller.process_echo(body)
