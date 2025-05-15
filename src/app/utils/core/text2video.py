import json
import os
import shutil
import jellyfish

from Ross_git.src.app.utils.NLP.parser import NLPParser
from Ross_git.src.app.utils.audio.remixer import SpeechMusicMixer
from Ross_git.src.app.utils.audio.tts import TextToSpeechSaver
from Ross_git.src.app.utils.images.downloader import ImageProcessor, download_images_sequentially
from Ross_git.src.app.utils.video.combiner import VideoCombiner
from Ross_git.src.app.utils.websearch.duck_go import DuckDuckGoImageSearcher


BACKGROUND_MUSIC_PATH = "/path/to/background_music.mp3"  # <-- Update this path


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
            sentence = sentence_obj.get('sentence', '')

            best_idx = None
            best_score = -1

            for i, img in enumerate(images):
                if assigned[i]:
                    continue
                title = img.get('title', '')
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
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def download(self, ordered_images):
        for idx, image_data in enumerate(ordered_images, start=1):
            filename = f"{idx:03}.png"
            image_data['output_filename'] = filename
            processor = ImageProcessor(image_data, output_dir=self.output_dir)
            processor.process()
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
            speech_length_ns=duration_ns
        )
        print("Mixed speech audio with background music.")


class VideoMaker:
    def __init__(self):
        self.combiner = VideoCombiner()

    def generate(self):
        self.combiner.generate_video()
        print("Generated final video.")


class VideoGenerator:
    def __init__(self, image_output_dir="output", max_image_results=100):
        self.image_searcher = ImageSearcher(max_results=max_image_results)
        self.text_parser = TextParser()
        self.image_orderer = ImageOrderer()
        self.image_downloader = ImageDownloader(output_dir=image_output_dir)
        self.tts = TextToSpeech()
        self.audio_mixer = AudioMixer()
        self.video_maker = VideoMaker()

        # Resolve absolute paths relative to this script's location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.tmp_dir = os.path.join(base_dir, "tmp")
        self.output_dir = os.path.join(base_dir, image_output_dir)

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
        download_images_sequentially(image_urls, output_dir=self.image_downloader.output_dir)
        self.image_downloader.download(ordered_images)

        speech_file, duration_ns = self.tts.synthesize(speech)
        self.audio_mixer.mix(speech_file, duration_ns)

        self.video_maker.generate()
        print("Video generation completed.")


if __name__ == "__main__":
    topic = "importance of cats"
    speech = """
    Cats have shared their lives with humans for thousands of years, weaving themselves into the fabric of our societies, cultures, and personal lives. Though often seen as independent and mysterious, cats have proven to be deeply important companions to humans in many ways. Their importance extends far beyond the simple pleasure of their purring presence on a lap. From their historical roles in pest control to their cultural symbolism, therapeutic benefits, and ecological influence, cats hold a significant place in our world.

    Historical and Cultural Significance
    The history of human-cat relationships dates back at least 9,000 years. The first evidence of domesticated cats was found on the Mediterranean island of Cyprus, where a cat was buried alongside a human. This early companionship hints at a practical relationship: cats helped control rodent populations in early agricultural communities, protecting stored grains from infestations.
    """

    generator = VideoGenerator()
    generator.generate_video(topic, speech)
