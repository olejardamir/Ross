import os
import uuid
from gtts import gTTS

class TextToSpeechSaver:
    def __init__(self, tmp_dir: str = "tmp", language: str = "en"):
        self.tmp_dir = tmp_dir
        self.language = language
        os.makedirs(self.tmp_dir, exist_ok=True)

    def synthesize(self, text: str, index: int, unique_id: str) -> str | None:
        """
        Converts text to speech and saves the audio file.

        Args:
        - text (str): Text to convert.
        - index (int): Sequence number for naming.
        - unique_id (str): UUID for uniqueness.

        Returns:
        - str | None: File path if successful, None on failure.
        """
        try:
            file_name = f"{unique_id}_{index}.mp3"
            file_path = os.path.join(self.tmp_dir, file_name)

            tts = gTTS(text=text, lang=self.language)
            tts.save(file_path)

            print(f"[INFO] Audio saved as '{file_path}'")
            return file_path

        except Exception as e:
            print(f"[ERROR] Failed to convert text to speech: {str(e)}")
            return None


if __name__ == "__main__":
    test_text = (
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry. "
        "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, "
        "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
    )

    tts_saver = TextToSpeechSaver()
    unique_id = str(uuid.uuid4())

    for index in range(1, 4):
        file_path = tts_saver.synthesize(test_text, index=index, unique_id=unique_id)
        if file_path:
            print(f"[INFO] File saved: {file_path}")
