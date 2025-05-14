import spacy

class NLPParser:
    """
    An object-oriented NLP parser that splits text into sentences and extracts
    root verbs, pronouns, common nouns, and proper nouns, excluding stopwords.
    """

    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            from spacy.cli import download
            download(model_name)
            self.nlp = spacy.load(model_name)

    def process(self, text: str) -> list[dict]:
        """
        Process the input text and return a list of dictionaries, each containing:
        - sentence: the sentence text
        - root_verbs: list of root verbs (non-stopwords)
        - pronouns: list of pronouns (non-stopwords)
        - common_nouns: list of common nouns (non-stopwords)
        - proper_nouns: list of proper nouns (non-stopwords)
        """
        doc = self.nlp(text)
        results = []

        for sent in doc.sents:
            root_verbs = [tok.text for tok in sent if tok.dep_ == "ROOT" and not tok.is_stop]
            pronouns = [tok.text for tok in sent if tok.pos_ == "PRON" and not tok.is_stop]
            common_nouns = [tok.text for tok in sent if tok.pos_ == "NOUN" and not tok.is_stop]
            proper_nouns = [tok.text for tok in sent if tok.pos_ == "PROPN" and not tok.is_stop]

            results.append({
                "sentence": sent.text.strip(),
                "root_verbs": root_verbs,
                "pronouns": pronouns,
                "common_nouns": common_nouns,
                "proper_nouns": proper_nouns
            })

        return results

    def display(self, results: list[dict]) -> None:
        """
        Nicely print the parsed sentences and their extracted root words.
        """
        print("Parsed Sentences with Roots, Pronouns, and Nouns (stopwords removed):")
        for idx, item in enumerate(results, start=1):
            print(f"{idx}. Sentence: {item['sentence']}")
            print(f"   Root Verb(s): {', '.join(item['root_verbs']) or 'None'}")
            print(f"   Pronouns: {', '.join(item['pronouns']) or 'None'}")
            print(f"   Common Nouns: {', '.join(item['common_nouns']) or 'None'}")
            print(f"   Proper Nouns: {', '.join(item['proper_nouns']) or 'None'}")


if __name__ == "__main__":
    parser = NLPParser()
    example = (
        "Alice gave Bob a book. "
        "He read it quickly, then traveled to Paris. "
        "Finally, the adventure ended."
    )
    results = parser.process(example)
    parser.display(results)
