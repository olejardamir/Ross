from pydub import AudioSegment
import os

class SpeechMusicMixer:
    def __init__(self, speech_path: str, music_path: str, output_path: str = "mixed_output.mp3"):
        self.speech_path = speech_path
        self.music_path = music_path
        self.output_path = output_path
        self.speech = None
        self.music = None
        self.mixed = None

    def load_audio(self):
        self.speech = AudioSegment.from_file(self.speech_path)
        self.music = AudioSegment.from_file(self.music_path)

    def process_music(self):
        # Reduce music volume by 6dB (~50%)
        self.music = self.music - 6

        # Ensure music is long enough
        target_duration = len(self.speech) + 1000  # +1s for fade-out
        while len(self.music) < target_duration:
            self.music += self.music

        # Trim and apply fade-in and fade-out
        self.music = self.music[:target_duration].fade_in(1000).fade_out(1000)

    def mix(self):
        # Mix speech over music with 1s offset
        self.mixed = self.music.overlay(self.speech, position=1000)

    def export(self):
        self.mixed.export(self.output_path, format="mp3")
        print(f"[INFO] Mixed audio saved to: {self.output_path}")

    def run(self):
        self.load_audio()
        self.process_music()
        self.mix()
        self.export()


if __name__ == "__main__":
    mixer = SpeechMusicMixer(
        speech_path="/home/coka/Desktop/Ross/Ross_git/src/app/utils/audio/tmp/6250064e-c0b0-46c9-b298-e5baf76c8603_1.mp3",
        music_path="/home/coka/Desktop/Ross/Ross_git/src/app/utils/audio/music/upbeat.mp3",
        output_path="mixed_output.mp3"
    )
    mixer.run()
