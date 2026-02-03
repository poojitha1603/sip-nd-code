import nltk
nltk.download('punkt')
import textstat
from bs4 import BeautifulSoup

def analyze_readability(text):
    flesch = textstat.flesch_reading_ease(text)
    grade = textstat.text_standard(text)

    if flesch >= 60:
        level = "Easy to read"
    elif flesch >= 40:
        level = "Moderate"
    else:
        level = "Difficult"

    return {
        "flesch_score": round(flesch, 2),
        "grade_level": grade,
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

    # Readability
    if readability["level"] == "Easy to read":
        score += 30
    elif readability["level"] == "Moderate":
        score += 20
        suggestions.append("👉 Simplify sentences to improve readability.")
    else:
        score += 10
        suggestions.append("👉 Use shorter sentences and simpler words.")

    # Accessibility
    if not accessibility_issues:
        score += 30
    else:
        score += max(0, 30 - len(accessibility_issues) * 10)
        suggestions.append(
            "👉 Fix accessibility issues like missing alt text and heading structure."
        )

    # Structure + mobile baseline
    score += 40

    return score, suggestions
