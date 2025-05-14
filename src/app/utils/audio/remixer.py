from pydub import AudioSegment
import os

def mix_speech_and_music(speech_path, music_path, output_path="mixed_output.mp3"):
    # Load files
    speech = AudioSegment.from_file(speech_path)
    music = AudioSegment.from_file(music_path)

    # Target durations
    speech_duration = len(speech)
    music_duration_needed = speech_duration + 1000  # +1s for fade-out

    # Reduce music volume by 6dB (~50%)
    music = music - 6

    # Repeat music to match duration
    while len(music) < music_duration_needed:
        music += music

    # Trim and apply fades
    music = music[:music_duration_needed].fade_in(1000).fade_out(1000)

    # Overlay speech at 1s (1000ms)
    mixed = music.overlay(speech, position=1000)

    # Export result
    mixed.export(output_path, format="mp3")
    print(f"[INFO] Mixed audio saved to: {output_path}")

# === Example usage ===
if __name__ == "__main__":
    mix_speech_and_music(
        speech_path="/home/coka/Desktop/Ross/Ross_git/src/app/utils/audio/tmp/6250064e-c0b0-46c9-b298-e5baf76c8603_1.mp3",   # Your speech file
        music_path="/home/coka/Desktop/Ross/Ross_git/src/app/utils/audio/music/upbeat.mp3",     # Your background music file
        output_path="mixed_output.mp3"
    )
