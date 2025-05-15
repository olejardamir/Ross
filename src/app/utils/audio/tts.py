import os
import uuid
from gtts import gTTS
from mutagen.mp3 import MP3

class TextToSpeechSaver:
    def __init__(self, tmp_dir: str = "tmp", language: str = "en"):
        # Resolve tmp_dir relative to this file location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.tmp_dir = os.path.join(base_dir, tmp_dir)
        self.language = language
        os.makedirs(self.tmp_dir, exist_ok=True)

    def synthesize(self, text: str, unique_id: str | None = None) -> tuple[str | None, int | None]:
        """
        Converts text to speech and saves the audio file.

        Args:
        - text (str): Text to convert.
        - unique_id (str | None): UUID for filename uniqueness (optional).

        Returns:
        - tuple[str | None, int | None]: (file name, length in nanoseconds) if successful,
          (None, None) on failure.
        """
        try:
            if unique_id is None:
                unique_id = str(uuid.uuid4())

            file_name = f"{unique_id}.mp3"
            file_path = os.path.join(self.tmp_dir, file_name)

            # Generate speech and save
            tts = gTTS(text=text, lang=self.language)
            tts.save(file_path)

            # Extract duration using mutagen
            audio = MP3(file_path)
            duration_sec = audio.info.length  # Duration in seconds (float)
            duration_ns = int(duration_sec * 1e9)  # Convert to nanoseconds

            print(f"[INFO] Audio saved as '{file_path}' with duration {duration_ns} ns")
            return file_name, duration_ns

        except Exception as e:
            print(f"[ERROR] Failed to convert text to speech: {str(e)}")
            return None, None


