import requests
from PIL import Image
from io import BytesIO
import os

class ImageProcessor:
    MIN_WIDTH = 640
    MIN_HEIGHT = 360
    TARGET_WIDTH = 1280
    TARGET_HEIGHT = 720

    def __init__(self, image_url, output_dir="."):
        self.image_url = image_url

        # Make output_dir absolute relative to this file's directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(base_dir, output_dir)

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
            int(self.image.height * scale_factor)
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


def download_images_sequentially(urls, output_dir="output"):
    for i, url in enumerate(urls):
        filename = f"{i:03d}.png"
        print(f"Processing {url} -> {filename}")
        processor = ImageProcessor(url, output_dir)
        saved_path = processor.process(filename)
        if saved_path is None:
            print(f"Skipped {url}")
        else:
            print(f"Successfully saved {saved_path}")
