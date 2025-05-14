import pprint
import time
from duckduckgo_search import DDGS


class DuckDuckGoImageSearcher:
    def __init__(self, prompt: str, max_results: int = 10):
        self.user_prompt = prompt
        self.max_results = max_results
        self.safe_domains = [
            "site:pexels.com",
            "site:pixabay.com",
            "site:unsplash.com",
            "site:commons.wikimedia.org",
        ]
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/113.0.0.0 Safari/537.36"
            )
        }

    def try_query(self, query):
        with DDGS(headers=self.headers) as ddgs:
            return list(ddgs.images(query, max_results=self.max_results))

    def search_images(self):
        for domain in self.safe_domains:
            query = f"{self.user_prompt} {domain}"
            print(f"[INFO] Trying query: {query}")
            try:
                results = self.try_query(query)
                if results:
                    return results
                else:
                    print("[WARN] No results, trying next domain...")
                time.sleep(2)  # Be polite
            except Exception as e:
                print(f"[WARN] Query failed: {e}, trying next domain...")
                time.sleep(2)
        raise RuntimeError("❌ All image search attempts failed or were rate-limited.")

    def display_results(self, results):
        print(f"\n--- Search results for: \"{self.user_prompt}\" ---\n")
        for i, image_data in enumerate(results, 1):
            print(f"\n=== Image #{i} ===")
            pprint.pprint(image_data)

    def run(self):
        try:
            results = self.search_images()
            self.display_results(results)
        except Exception as e:
            print(f"❌ Final error: {e}")


if __name__ == "__main__":
    searcher = DuckDuckGoImageSearcher(prompt="quantum physics", max_results=5)
    searcher.run()
