"""365 unique affirmation generator with themed monthly batches."""

import random
from datetime import date, timedelta
from typing import List, Dict, Set


THEMES = [
    "confidence", "focus", "gratitude", "discipline",
    "peace", "resilience", "growth", "leadership",
    "clarity", "courage", "balance", "purpose",
    "kindness", "patience", "energy", "wisdom",
]

TEMPLATES = [
    "I am building {theme} one day at a time.",
    "My {theme} grows stronger with every choice I make.",
    "I trust myself to create a life filled with {theme}.",
    "Each day I move forward with {theme} and intention.",
    "I welcome {theme} into my thoughts, actions, and decisions.",
    "I am becoming more aligned with {theme} every day.",
    "My consistency creates lasting {theme}.",
    "I carry {theme} into everything I do today.",
    "Today I choose {theme} over doubt.",
    "My path is paved with {theme} and determination.",
]

MONTH_THEMES: Dict[int, str] = {
    1: "fresh starts", 2: "self-worth", 3: "discipline",
    4: "growth", 5: "momentum", 6: "peace",
    7: "confidence", 8: "clarity", 9: "focus",
    10: "resilience", 11: "gratitude", 12: "purpose",
}


def generate_affirmation(theme: str | None = None) -> str:
    """Generate a single affirmation from a theme and template."""
    selected_theme = theme or random.choice(THEMES)
    template = random.choice(TEMPLATES)
    return template.format(theme=selected_theme)


def generate_year_affirmations(year: int) -> List[Dict]:
    """Generate 365 (or 366) unique affirmations for a full year.

    Strategy:
    1. Each month has a primary theme (60% weight)
    2. Random themes fill the rest (40% weight)
    3. Uniqueness guaranteed via set tracking
    4. Leap year automatically handled via date math
    """
    start = date(year, 1, 1)
    end = date(year + 1, 1, 1)
    days = (end - start).days

    results: List[Dict] = []
    used_texts: Set[str] = set()
    max_attempts = 100

    for i in range(days):
        day_date = start + timedelta(days=i)
        month_theme = MONTH_THEMES.get(day_date.month)

        for attempt in range(max_attempts):
            if month_theme and random.random() > 0.4:
                theme = month_theme
            else:
                theme = random.choice(THEMES)

            text = generate_affirmation(theme)
            key = text.lower().strip()

            if key not in used_texts:
                used_texts.add(key)
                results.append({"date": day_date, "theme": theme, "text": text})
                break
        else:
            theme = month_theme or random.choice(THEMES)
            text = f"Day {i+1}: I embrace {theme} fully and completely."
            results.append({"date": day_date, "theme": theme, "text": text})

    return results
