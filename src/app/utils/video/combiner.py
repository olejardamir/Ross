import os
import subprocess

class VideoCombiner:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.img_dir = os.path.abspath(os.path.join(self.base_dir, "../core/output"))
        self.audio_path = os.path.abspath(os.path.join(self.base_dir, "../core/tmp/mixed_output.mp3"))
        self.output_path = os.path.abspath(os.path.join(self.base_dir, "../core/tmp/final_output.mp4"))

    def get_audio_duration_seconds(self):
        if not os.path.exists(self.audio_path):
            raise FileNotFoundError(f"Audio file not found at: {self.audio_path}")

        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                self.audio_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"ffprobe error:\n{result.stdout}")

        try:
            duration = float(result.stdout.strip())
            return duration
        except ValueError:
            raise RuntimeError(f"Could not parse duration from ffprobe output:\n{result.stdout}")

    def generate_ffmpeg_input_file(self, duration_per_image):
        input_list_path = os.path.join(self.img_dir, "input.txt")
        images = sorted(f for f in os.listdir(self.img_dir) if f.endswith(".png"))
        if not images:
            raise RuntimeError(f"No .png images found in {self.img_dir}")

        with open(input_list_path, "w") as f:
            for image in images:
                f.write(f"file '{image}'\n")
                f.write(f"duration {duration_per_image:.2f}\n")
            # Write last image file again to prevent frame drop on last image
            f.write(f"file '{images[-1]}'\n")

        return input_list_path

    def generate_video(self):
        print(f"Audio file path: {self.audio_path}")
        print(f"Images directory: {self.img_dir}")
        print(f"Output video path: {self.output_path}")

        duration = self.get_audio_duration_seconds()
        print(f"Audio duration (seconds): {duration}")

        images = sorted(f for f in os.listdir(self.img_dir) if f.endswith(".png"))
        if len(images) < 2:
            raise RuntimeError("Need at least 2 images for slideshow.")

        duration_per_image = duration / len(images)
        input_txt_path = self.generate_ffmpeg_input_file(duration_per_image)

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", input_txt_path,
            "-i", self.audio_path,
            "-vf", f"fade=t=in:st=0:d=1,fade=t=out:st={duration-1:.2f}:d=1",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            "-shortest",
            self.output_path
        ]

        print("Running ffmpeg command...")
        subprocess.run(cmd, cwd=self.img_dir, check=True)
        print(f"✅ Video saved at: {self.output_path}")



