def calculate_severity(story: str, truth: int, case_type: str) -> int:
    """
    Rule-based severity scorer (0–100)
    """
    score = 0
    story = story.lower()

    keywords = {
        "Violence": ["hit", "attack", "knife", "murder"],
        "Cyber Crime": ["hack", "fraud", "scam", "otp"],
        "Theft": ["steal", "rob"],
        "Harassment": ["abuse", "threat", "blackmail"]
    }

    for key, words in keywords.items():
        if case_type == key or any(w in story for w in words):
            score += 20

    score += int(truth * 0.2)
    return min(score, 100)
