import os
from gtts import gTTS
import uuid


# Function to convert text to speech and save to tmp directory
def text_to_speech(text: str, index: int, unique_id: str):
    """
    Converts text to speech and saves it as an MP3 file in the 'tmp' directory with a unique name.

    Args:
    - text (str): The text to convert into speech.
    - index (int): The index number (used for file naming).
    - unique_id (str): The UUID to append to the filename for uniqueness.

    Returns:
    - str: Path to the saved audio file.
    """
    try:
        # Ensure 'tmp' directory exists
        tmp_dir = "tmp"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        # Generate a unique filename using UUID and index
        file_name = f"{unique_id}_{index}.mp3"
        file_path = os.path.join(tmp_dir, file_name)

        # Create a gTTS object and save the audio file
        tts = gTTS(text=text, lang='en')
        tts.save(file_path)
        print(f"[INFO] Audio saved as '{file_path}'")

        return file_path

    except Exception as e:
        print(f"[ERROR] Failed to convert text to speech: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # The text you want to convert
    test_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

    # Generate a unique UUID
    unique_id = str(uuid.uuid4())

    # Example: Creating the first, second, and third audio files
    for index in range(1, 2):
        file_path = text_to_speech(test_text, index, unique_id)
        if file_path:
            print(f"[INFO] File saved: {file_path}")
