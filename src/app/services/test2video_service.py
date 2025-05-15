from Ross_git.src.app.controllers.text2video_controller import Text2VideoController

class Text2VideoService:
    def __init__(self, controller: Text2VideoController):
        self.controller = controller

    def create_video(self, topic: str, speech: str) -> None:
        self.controller.generate_video(topic, speech)
