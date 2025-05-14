import requests
from PIL import Image
from io import BytesIO
import uuid
import os

class ImageProcessor:
    MIN_WIDTH = 640
    MIN_HEIGHT = 360
    TARGET_WIDTH = 1280
    TARGET_HEIGHT = 720

    def __init__(self, data, output_dir="."):
        self.data = data
        self.output_dir = output_dir
        self.image = None
        self.resized_image = None
        self.final_image = None

    def is_size_valid(self):
        return self.data['width'] >= self.MIN_WIDTH and self.data['height'] >= self.MIN_HEIGHT

    def download_image(self):
        try:
            response = requests.get(self.data['image'], timeout=10)
            response.raise_for_status()
            self.image = Image.open(BytesIO(response.content)).convert("RGB")
            return True
        except Exception as e:
            print(f"Download or open failed: {e}")
            return False

    def resize_and_crop(self):
        if self.image is None:
            raise ValueError("Image not loaded")

        img_ratio = self.image.width / self.image.height
        target_ratio = self.TARGET_WIDTH / self.TARGET_HEIGHT

        if img_ratio > target_ratio:
            # Wider image: resize by height
            scale_factor = self.TARGET_HEIGHT / self.image.height
        else:
            # Taller image: resize by width
            scale_factor = self.TARGET_WIDTH / self.image.width

        new_size = (
            int(self.image.width * scale_factor),
            int(self.image.height * scale_factor)
        )
        self.resized_image = self.image.resize(new_size, Image.BICUBIC)

        # Center crop
        left = (self.resized_image.width - self.TARGET_WIDTH) // 2
        top = (self.resized_image.height - self.TARGET_HEIGHT) // 2
        right = left + self.TARGET_WIDTH
        bottom = top + self.TARGET_HEIGHT

        self.final_image = self.resized_image.crop((left, top, right, bottom))

    def save_image(self):
        if self.final_image is None:
            raise ValueError("Final image not prepared")
        os.makedirs(self.output_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(self.output_dir, filename)
        self.final_image.save(filepath, format="PNG")
        print(f"Saved image: {filepath}")
        return filepath

    def process(self):
        if not self.is_size_valid():
            print("Image too small. Skipping.")
            return None
        if not self.download_image():
            return None
        self.resize_and_crop()
        return self.save_image()


# Example usage:
if __name__ == "__main__":
    image_data = {
        'height': 1026,
        'image': 'http://4.bp.blogspot.com/-6Gur5leMULA/UW7clZ7VTLI/AAAAAAAAhxI/YEN6kYrK20Y/s1600/funny-cat-pictures-046-019.jpg',
        'source': 'Bing',
        'thumbnail': 'https://tse1.mm.bing.net/th?id=OIP.b75wsUso03rbXnv0EQoSXwHaE9&pid=Api',
        'title': 'Funny cats - part 46 (30 pics + 10 gifs) | Amazing Creatures',
        'url': 'http://amazing-creature.blogspot.com/2013/04/funny-cats-part-46-30-pics-10-gifs.html',
        'width': 1533
    }

    processor = ImageProcessor(image_data, output_dir="output")
    processor.process()
