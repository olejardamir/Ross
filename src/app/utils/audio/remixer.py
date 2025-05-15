import os
from pydub import AudioSegment

class SpeechMusicMixer:
    def __init__(self, speech_path: str, music_path: str, output_path: str = "mixed_output.mp3", speech_length_ms: int = None):
        self.speech_path = speech_path
        self.music_path = music_path
        self.output_path = output_path
        self.speech_length_ms = speech_length_ms
        self.speech = None
        self.music = None
        self.mixed = None

    def load_audio(self):
        self.speech = AudioSegment.from_file(self.speech_path)
        self.music = AudioSegment.from_file(self.music_path)

    def process_music(self):
        self.music = self.music - 9.13  # Reduce volume to about 35%
        target_duration = len(self.speech) + 1000  # +1s for fade-out
        while len(self.music) < target_duration:
            self.music += self.music
        self.music = self.music[:target_duration].fade_in(1000).fade_out(1000)

    def mix(self):
        self.mixed = self.music.overlay(self.speech, position=1000)

    def export(self):
        self.mixed.export(self.output_path, format="mp3")
        print(f"[INFO] Mixed audio saved to: {self.output_path}")

    def run(self):
        self.load_audio()
        self.process_music()
        self.mix()
        self.export()

    @staticmethod
    def mix_speech_with_music(speech_rel_path: str, speech_length_ns: int):
        # Get absolute directory of this remixer.py file
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Resolve speech and music paths relative to remixer.py location
        speech_path = os.path.join(base_dir, "tmp", speech_rel_path)
        music_path = os.path.join(base_dir, "..", "audio", "music", "uplifting_guitar.mp3")
        output_path = os.path.join(base_dir, "tmp", "mixed_output.mp3")
        speech_length_ms = speech_length_ns // 1_000_000

        mixer = SpeechMusicMixer(
            speech_path=speech_path,
            music_path=music_path,
            output_path=output_path,
            speech_length_ms=speech_length_ms
        )
        mixer.run()
