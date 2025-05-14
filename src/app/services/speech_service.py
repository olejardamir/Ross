from Ross_git.src.app.controllers.speech_controller import SpeechController

class SpeechService:
    def __init__(self, controller: SpeechController):
        self.controller = controller

    def create_speech(self, topic: str) -> str:
        return self.controller.generate_speech(topic)
