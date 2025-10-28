

import re
import json
import requests
from typing import List, Dict, Tuple
from collections import Counter
import string


class TextPreprocessor:

    def __init__(self):
        # Gutenberg markers (these are common, add more if needed)
        self.gutenberg_markers = [
            "*** START OF THIS PROJECT GUTENBERG",
            "*** END OF THIS PROJECT GUTENBERG",
            "*** START OF THE PROJECT GUTENBERG",
            "*** END OF THE PROJECT GUTENBERG",
            "*END*THE SMALL PRINT",
            "<<THIS ELECTRONIC VERSION"
        ]

    def clean_text(self, text: str) -> str:
        """
        Clean the text by removing punctuation and extra whitespace safely
        """
        try:
            # ✅ Only remove non-word, non-space characters safely
            text = re.sub(r"[^\w\s]", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            return text
        except re.error as e:
            raise Exception(f"Regex error during text cleaning: {e}")

    def normalize_text(self, text: str, preserve_sentences: bool = True) -> str:
        """
        Normalize text while preserving sentence boundaries

        Args:
            text: Input text
            preserve_sentences: If True, keeps . ! ? for sentence detection
        """
        # Convert to lowercase
        text = text.lower()

        # Standardize quotes and dashes
        text = re.sub(r'[""]', '"', text)
        text = re.sub(r"[‘’]", "'", text)
        text = re.sub(r'—|–', '-', text)

        if preserve_sentences:
            # Keep sentence endings but remove other punctuation
            text = re.sub(r'[^\w\s.!?\'-]', ' ', text)
        else:
            # Remove all punctuation except apostrophes in contractions
            text = re.sub(r"(?<!\w)'(?!\w)|[^\w\s]", ' ', text)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def tokenize_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def tokenize_words(self, text: str) -> List[str]:
        """Split text into words"""
        text_for_words = re.sub(r'[.!?]', '', text)
        words = text_for_words.split()
        words = [w for w in words if w]
        return words

    def tokenize_chars(self, text: str, include_space: bool = True) -> List[str]:
        """Split text into characters"""
        if include_space:
            text = re.sub(r'\s+', ' ', text)
            return list(text)
        else:
            return [c for c in text if c != ' ']

    def get_sentence_lengths(self, sentences: List[str]) -> List[int]:
        """Get word count for each sentence"""
        return [len(self.tokenize_words(sent)) for sent in sentences]

    # ==============================
    # NEW METHODS FOR ASSIGNMENT
    # ==============================

    def fetch_from_url(self, url: str) -> str:
        """
        Fetch text content from a URL (especially Project Gutenberg)

        Args:
            url: URL to a .txt file

        Returns:
            Raw text content

        Raises:
            Exception if URL is invalid or cannot be reached
        """
        # Validate URL format
        if not url.lower().endswith(".txt"):
            raise Exception("URL must point to a .txt file")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching URL: {e}")

    def get_text_statistics(self, text: str) -> Dict:
        """
        Calculate basic statistics about the text

        Returns dictionary with:
            - total_characters
            - total_words  
            - total_sentences
            - avg_word_length
            - avg_sentence_length
            - most_common_words (top 10)
        """
        words = self.tokenize_words(text)
        sentences = self.tokenize_sentences(text)

        total_characters = len(text)
        total_words = len(words)
        total_sentences = len(sentences)

        avg_word_length = (sum(len(w) for w in words) /
                           total_words) if total_words > 0 else 0
        avg_sentence_length = (sum(len(self.tokenize_words(
            s)) for s in sentences) / total_sentences) if total_sentences > 0 else 0

        word_counts = Counter(words)
        most_common_words = word_counts.most_common(10)

        return {
            "total_characters": total_characters,
            "total_words": total_words,
            "total_sentences": total_sentences,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "most_common_words": most_common_words
        }

    def create_summary(self, text: str, num_sentences: int = 3) -> str:
        """
        Create a simple extractive summary by returning the first N sentences

        Args:
            text: Cleaned text
            num_sentences: Number of sentences to include

        Returns:
            Summary string
        """
        sentences = self.tokenize_sentences(text)
        if not sentences:
            return ""

        summary_sentences = sentences[:num_sentences]
        summary = ". ".join(summary_sentences)

        if not summary.endswith(('.', '!', '?')):
            summary += '.'

        return summary


class FrequencyAnalyzer:
    """Calculate n-gram frequencies from tokenized text"""

    def calculate_ngrams(self, tokens: List[str], n: int) -> Dict[Tuple[str, ...], int]:
        """Calculate n-gram frequencies"""
        if n == 1:
            return dict(Counter(tokens))

        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i + n])
            ngrams.append(ngram)

        return dict(Counter(ngrams))

    def calculate_probabilities(self, ngram_counts: Dict, smoothing: float = 0.0) -> Dict:
        """Convert counts to probabilities"""
        total = sum(ngram_counts.values()) + smoothing * len(ngram_counts)

        probabilities = {}
        for ngram, count in ngram_counts.items():
            probabilities[ngram] = (count + smoothing) / total

        return probabilities

    def save_frequencies(self, frequencies: Dict, filename: str):
        """Save frequency dictionary to JSON file"""
        json_friendly = {}
        for key, value in frequencies.items():
            if isinstance(key, tuple):
                json_friendly['||'.join(key)] = value
            else:
                json_friendly[key] = value

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_friendly, f, indent=2, ensure_ascii=False)

    def load_frequencies(self, filename: str) -> Dict:
        """Load frequency dictionary from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        frequencies = {}
        for key, value in json_data.items():
            if '||' in key:
                frequencies[tuple(key.split('||'))] = value
            else:
                frequencies[key] = value

        return frequencies


# Example usage to test your setup
if __name__ == "__main__":
    # Test with a small example
    sample_text = """
    This is a test. This is only a test! 
    If this were a real emergency, you would be informed.
    """

    preprocessor = TextPreprocessor()
    analyzer = FrequencyAnalyzer()

    # Clean and normalize
    clean_text = preprocessor.normalize_text(sample_text)
    print(f"Cleaned text: {clean_text}\n")

    # Get sentences
    sentences = preprocessor.tokenize_sentences(clean_text)
    print(f"Sentences: {sentences}\n")

    # Get words
    words = preprocessor.tokenize_words(clean_text)
    print(f"Words: {words}\n")

    # Calculate bigrams
    bigrams = analyzer.calculate_ngrams(words, 2)
    print(f"Word bigrams: {bigrams}\n")

    # Calculate character trigrams
    chars = preprocessor.tokenize_chars(clean_text)
    char_trigrams = analyzer.calculate_ngrams(chars, 3)
    print(
        f"Character trigrams (first 5): {dict(list(char_trigrams.items())[:5])}")

    print("\n✅ Basic functionality working!")

    # --- Test new methods ---
    print("\n--- Testing new methods ---")

    stats = preprocessor.get_text_statistics(clean_text)
    print("Text Statistics:", json.dumps(stats, indent=2))

    summary = preprocessor.create_summary(sample_text, num_sentences=2)
    print("\nSummary:", summary)
