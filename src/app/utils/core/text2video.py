# 1. we search for the images based on a short text, lets say "Importance of oxygen", removing images smaller than ???
# 2. we parse sentences of the larger text, 900 words approx on the importance of oxygen.
# 3. we order the images using jaro distance to match the order of the sentences
# 4. we make the tts for larger text (non parsed)
# 5. we combine it with music
# 6. we combine the images into a video of length that matches the audio length
# 7. we add the audio and video together (we need to deal with small mismatches, maybe making a video a bit longer?)
import json
import os

import jellyfish

from Ross_git.src.app.utils.NLP.parser import NLPParser
from Ross_git.src.app.utils.audio.remixer import SpeechMusicMixer
from Ross_git.src.app.utils.audio.tts import TextToSpeechSaver
from Ross_git.src.app.utils.images.downloader import ImageProcessor, download_images_sequentially
from Ross_git.src.app.utils.websearch.duck_go import DuckDuckGoImageSearcher


def search_duckduckgo_images(query: str, max_results: int = 100):
    searcher = DuckDuckGoImageSearcher(prompt=query, max_results=max_results)
    results = searcher.run()
    print(json.dumps(results, indent=2))
    return results


def parse_text_with_nlp(text: str):
    parser = NLPParser()
    results = parser.process(text)
    print(results)
    return results


def order_images_by_sentence_similarity(parsed_sentences, duck_results):
    assigned = [False] * len(duck_results)
    ordered_results = []

    for sentence_obj in parsed_sentences:
        sentence = sentence_obj.get('sentence', '')

        best_index = None
        best_score = -1

        for i, image_obj in enumerate(duck_results):
            if assigned[i]:
                continue
            title = image_obj.get('title', '')
            score = jellyfish.jaro_similarity(sentence.lower(), title.lower())  # <--- corrected here
            if score > best_score:
                best_score = score
                best_index = i

        if best_index is not None:
            assigned[best_index] = True
            ordered_results.append(duck_results[best_index])

    # Append leftover images that were not matched
    for i, was_assigned in enumerate(assigned):
        if not was_assigned:
            ordered_results.append(duck_results[i])

    return ordered_results


def download_ordered_images_sequentially(ordered_images, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, image_data in enumerate(ordered_images, start=1):
        # Prepare filename with zero-padded numbering
        filename = f"{idx:03}.png"

        # Add or override output filename in image_data (assuming your ImageProcessor supports it)
        # If ImageProcessor expects output_dir only and uses url or title for filename,
        # you may need to adapt ImageProcessor to accept filename or implement saving logic here.

        # For demonstration, let's assume ImageProcessor uses output_dir and the filename attribute
        image_data['output_filename'] = filename

        processor = ImageProcessor(image_data, output_dir=output_dir)
        processor.process()

    print(f"Downloaded {len(ordered_images)} images to '{output_dir}'")

def extract_image_urls(ordered_images):
    return [item["image"] for item in ordered_images if "image" in item and item["image"]]

def tts(text):
    tts_saver = TextToSpeechSaver()
    file_name, duration_ns = tts_saver.synthesize(bigtext)
    return file_name, duration_ns


if __name__ == "__main__":
    smalltext = "importance of cats"
    bigtext = """

    Cats have shared their lives with humans for thousands of years, weaving themselves into the fabric of our societies, cultures, and personal lives. Though often seen as independent and mysterious, cats have proven to be deeply important companions to humans in many ways. Their importance extends far beyond the simple pleasure of their purring presence on a lap. From their historical roles in pest control to their cultural symbolism, therapeutic benefits, and ecological influence, cats hold a significant place in our world.

Historical and Cultural Significance
The history of human-cat relationships dates back at least 9,000 years. The first evidence of domesticated cats was found on the Mediterranean island of Cyprus, where a cat was buried alongside a human. This early companionship hints at a practical relationship: cats helped control rodent populations in early agricultural communities, protecting stored grains from infestations.

    """

    # duck_results = search_duckduckgo_images(smalltext)
    # parsed_text = parse_text_with_nlp(bigtext)
    # ordered_images = order_images_by_sentence_similarity(parsed_text, duck_results)
    # image_urls = extract_image_urls(ordered_images)
    # download_images_sequentially(image_urls)

    file_name, duration_ns = tts(bigtext)
    SpeechMusicMixer.mix_speech_with_music(
        speech_rel_path=file_name,
        speech_length_ns=duration_ns
    )