from Ross_git.src.app.utils.core.text2video import VideoGenerator

class Text2VideoController:
    def generate_video(self, topic: str, speech: str) -> None:
        # Use topic as short_text, speech as long_text
        generator = VideoGenerator()
        generator.generate_video(topic, speech)
