from bs4 import BeautifulSoup
import re

def analyze_readability(text):
    sentences = re.split(r'[.!?]', text)
    words = re.findall(r'\w+', text)

    num_sentences = max(1, len(sentences))
    num_words = max(1, len(words))
    avg_words_per_sentence = num_words / num_sentences

    if avg_words_per_sentence < 15:
        level = "Easy to read"
        score = 65
    elif avg_words_per_sentence < 25:
        level = "Moderate"
        score = 45
    else:
        level = "Difficult"
        score = 25

    return {
        "flesch_score": score,
        "grade_level": "Approximate",
        "level": level
    }

def analyze_accessibility(html):
    soup = BeautifulSoup(html, "html.parser")
    issues = []

    images = soup.find_all("img")
    if any(not img.get("alt") for img in images):
        issues.append("Some images are missing alt text")

    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 0:
        issues.append("No h1 heading found")
    elif len(h1_tags) > 1:
        issues.append("Multiple h1 headings found")

    return issues

def calculate_usability_score(readability, accessibility_issues):
    score = 0
    suggestions = []

    if readability["level"] == "Easy to read":
        score += 30
    elif readability["level"] == "Moderate":
        score += 20
        suggestions.append("👉 Simplify sentences to improve readability.")
    else:
        score += 10
        suggestions.append("👉 Use shorter sentences and simpler words.")

    if not accessibility_issues:
        score += 30
    else:
        score += max(0, 30 - len(accessibility_issues) * 10)
        suggestions.append(
            "👉 Fix accessibility issues like missing alt text and heading structure."
        )

    score += 40
    return score, suggestions
