from Ross_git.src.app.utils.NLP.speech_generator import generate_full_speech

class SpeechController:
    def generate_speech(self, topic: str) -> str:
        speech = generate_full_speech(topic)
        return speech
