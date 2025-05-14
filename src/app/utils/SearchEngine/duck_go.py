import pprint
from duckduckgo_search import DDGS


class DuckDuckGoImageSearcher:
    def __init__(self, prompt: str, max_results: int = 10):
        self.prompt = prompt
        self.max_results = max_results
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/113.0.0.0 Safari/537.36"
            )
        }

    def search_images(self):
        with DDGS(headers=self.headers) as ddgs:
            results = ddgs.images(self.prompt, max_results=self.max_results)
            return list(results)

    def display_results(self, results):
        print(f"\n--- Search results for: \"{self.prompt}\" ---\n")
        for i, image_data in enumerate(results, 1):
            print(f"\n=== Image #{i} ===")
            pprint.pprint(image_data)

    def run(self):
        try:
            results = self.search_images()
            self.display_results(results)
        except Exception as e:
            print(f"❌ Error occurred during image search: {e}")


if __name__ == "__main__":
    searcher = DuckDuckGoImageSearcher(prompt="funny kittens", max_results=5)
    searcher.run()
