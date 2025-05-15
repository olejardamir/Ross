import requests
from PIL import Image
from io import BytesIO
import os
import shutil
import json
import jellyfish

from Ross_git.src.app.utils.NLP.parser import NLPParser
from Ross_git.src.app.utils.audio.remixer import SpeechMusicMixer
from Ross_git.src.app.utils.audio.tts import TextToSpeechSaver
from Ross_git.src.app.utils.images.downloader import ImageProcessor, download_images_sequentially
from Ross_git.src.app.utils.video.combiner import VideoCombiner
from Ross_git.src.app.utils.websearch.duck_go import DuckDuckGoImageSearcher


BACKGROUND_MUSIC_PATH = "/path/to/background_music.mp3"  # <-- Update this path


class ImageProcessor:
    MIN_WIDTH = 640
    MIN_HEIGHT = 360
    TARGET_WIDTH = 1280
    TARGET_HEIGHT = 720

    def __init__(self, image_url, output_dir="."):
        self.image_url = image_url
        # Resolve absolute path based on this script location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = (
            output_dir if os.path.isabs(output_dir) else os.path.join(base_dir, output_dir)
        )
        self.image = None
        self.resized_image = None
        self.final_image = None

    def download_image(self):
        try:
            response = requests.get(self.image_url, timeout=10)
            response.raise_for_status()
            self.image = Image.open(BytesIO(response.content)).convert("RGB")
            return True
        except Exception as e:
            print(f"Failed to download/open image from {self.image_url}: {e}")
            return False

    def is_size_valid(self):
        if self.image is None:
            return False
        return self.image.width >= self.MIN_WIDTH and self.image.height >= self.MIN_HEIGHT

    def resize_and_crop(self):
        img_ratio = self.image.width / self.image.height
        target_ratio = self.TARGET_WIDTH / self.TARGET_HEIGHT

        if img_ratio > target_ratio:
            scale_factor = self.TARGET_HEIGHT / self.image.height
        else:
            scale_factor = self.TARGET_WIDTH / self.image.width

        new_size = (
            int(self.image.width * scale_factor),
            int(self.image.height * scale_factor),
        )
        self.resized_image = self.image.resize(new_size, Image.BICUBIC)

        left = (self.resized_image.width - self.TARGET_WIDTH) // 2
        top = (self.resized_image.height - self.TARGET_HEIGHT) // 2
        right = left + self.TARGET_WIDTH
        bottom = top + self.TARGET_HEIGHT

        self.final_image = self.resized_image.crop((left, top, right, bottom))

    def save_image(self, filename):
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        self.final_image.save(filepath, format="PNG")
        print(f"Saved image: {filepath}")
        return filepath

    def process(self, filename):
        if not self.download_image():
            return None
        if not self.is_size_valid():
            print(f"Image too small: {self.image.width}x{self.image.height}. Skipping.")
            return None
        self.resize_and_crop()
        return self.save_image(filename)


def download_images_sequentially(urls, output_dir="."):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_output_dir = output_dir if os.path.isabs(output_dir) else os.path.join(base_dir, output_dir)
    for i, url in enumerate(urls):
        filename = f"{i:03d}.png"
        print(f"Processing {url} -> {filename}")
        processor = ImageProcessor(url, abs_output_dir)
        saved_path = processor.process(filename)
        if saved_path is None:
            print(f"Skipped {url}")
        else:
            print(f"Successfully saved {saved_path}")


class ImageSearcher:
    def __init__(self, max_results=100):
        self.max_results = max_results

    def search(self, query):
        searcher = DuckDuckGoImageSearcher(prompt=query, max_results=self.max_results)
        results = searcher.run()
        print(f"Image search results for '{query}':")
        print(json.dumps(results, indent=2))
        return results


class TextParser:
    def __init__(self):
        self.parser = NLPParser()

    def parse(self, text):
        parsed = self.parser.process(text)
        print(f"Parsed text into {len(parsed)} sentence objects")
        return parsed


class ImageOrderer:
    def __init__(self):
        pass

    def order(self, parsed_sentences, images):
        assigned = [False] * len(images)
        ordered = []

        for sentence_obj in parsed_sentences:
            sentence = sentence_obj.get("sentence", "")

            best_idx = None
            best_score = -1

            for i, img in enumerate(images):
                if assigned[i]:
                    continue
                title = img.get("title", "")
                score = jellyfish.jaro_similarity(sentence.lower(), title.lower())
                if score > best_score:
                    best_score = score
                    best_idx = i

            if best_idx is not None:
                assigned[best_idx] = True
                ordered.append(images[best_idx])

        # Append images not matched
        for i, assigned_flag in enumerate(assigned):
            if not assigned_flag:
                ordered.append(images[i])

        return ordered


class ImageDownloader:
    def __init__(self, output_dir):
        # output_dir is absolute path
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def download(self, ordered_images):
        for idx, image_data in enumerate(ordered_images, start=1):
            filename = f"{idx:03}.png"
            image_data["output_filename"] = filename
            processor = ImageProcessor(image_data["image"], output_dir=self.output_dir)
            processor.process(filename)
        print(f"Downloaded {len(ordered_images)} images to '{self.output_dir}'")

    def extract_urls(self, images):
        return [img["image"] for img in images if "image" in img and img["image"]]


class TextToSpeech:
    def __init__(self):
        self.tts_saver = TextToSpeechSaver()

    def synthesize(self, text):
        filename, duration_ns = self.tts_saver.synthesize(text)
        print(f"Generated speech audio: {filename}, duration: {duration_ns} ns")
        return filename, duration_ns


class AudioMixer:
    def mix(self, speech_file, duration_ns, music_path=BACKGROUND_MUSIC_PATH):
        mixer = SpeechMusicMixer(speech_path=speech_file, music_path=music_path)
        mixer.mix_speech_with_music(
            speech_rel_path=speech_file,
            speech_length_ns=duration_ns,
        )
        print("Mixed speech audio with background music.")


class VideoMaker:
    def __init__(self):
        self.combiner = VideoCombiner()

    def generate(self):
        self.combiner.generate_video()
        print("Generated final video.")


class VideoGenerator:
    def __init__(
        self,
        image_output_dir="output",
        image_tmp_dir="tmp",
        max_image_results=100,
    ):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # this file's dir

        # Assuming this script is inside Ross_git/src/app/utils/core/
        self.output_dir = os.path.join(base_dir, image_output_dir)
        self.tmp_dir = os.path.join(base_dir, image_tmp_dir)

        self.image_searcher = ImageSearcher(max_results=max_image_results)
        self.text_parser = TextParser()
        self.image_orderer = ImageOrderer()

        # pass absolute output_dir to ImageDownloader
        self.image_downloader = ImageDownloader(output_dir=self.output_dir)

        self.tts = TextToSpeech()
        self.audio_mixer = AudioMixer()
        self.video_maker = VideoMaker()

    def _clean_dirs(self):
        for folder in [self.tmp_dir, self.output_dir]:
            if os.path.exists(folder):
                print(f"Cleaning directory: {folder}")
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")

    def generate_video(self, topic, speech):
        self._clean_dirs()
        print("Starting video generation workflow...")

        duck_results = self.image_searcher.search(topic)
        parsed_sentences = self.text_parser.parse(speech)
        ordered_images = self.image_orderer.order(parsed_sentences, duck_results)

        image_urls = self.image_downloader.extract_urls(ordered_images)

        download_images_sequentially(image_urls, output_dir=self.output_dir)
        self.image_downloader.download(ordered_images)

        speech_file, duration_ns = self.tts.synthesize(speech)
        self.audio_mixer.mix(speech_file, duration_ns)

        self.video_maker.generate()
        print("Video generation completed.")
