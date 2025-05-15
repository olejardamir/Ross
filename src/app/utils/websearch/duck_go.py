from duckduckgo_search import DDGS


class DuckDuckGoImageSearcher:
    def __init__(self, prompt: str, max_results: int = 100):
        self.user_prompt = prompt
        self.max_results = max_results
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/113.0.0.0 Safari/537.36"
            )
        }

    def try_query(self, query, fetch_results=300):
        with DDGS(headers=self.headers) as ddgs:
            return list(ddgs.images(query, max_results=fetch_results))

    def filter_by_min_size(self, images, min_width=640, min_height=360):
        filtered = []
        for img in images:
            width = img.get('width')
            height = img.get('height')
            if width is not None and height is not None:
                try:
                    w = int(width)
                    h = int(height)
                    if w >= min_width and h >= min_height:
                        filtered.append(img)
                except ValueError:
                    continue
        return filtered

    def search_images(self):
        query = self.user_prompt
        try:
            raw_results = self.try_query(query, fetch_results=300)
            if raw_results:
                filtered_results = self.filter_by_min_size(raw_results)
                if filtered_results:
                    return filtered_results[:self.max_results]
                else:
                    print("[WARN] No images meet the minimum size requirements.")
                    return []
            else:
                print("[WARN] No results found.")
                return []
        except Exception as e:
            print(f"[WARN] Query failed: {e}")
            return []

    def run(self):
        # Return the filtered list instead of printing
        return self.search_images()



