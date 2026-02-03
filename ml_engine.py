def calculate_severity(story: str, truth: int, case_type: str) -> int:
    """
    Rule-based ML severity scorer (0–100)
    """
    score = 0
    text = story.lower()

    keywords = {
        "Violence": ["attack", "hit", "knife", "blood"],
        "Murder": ["murder", "kill", "death"],
        "Cyber Crime": ["hack", "fraud", "scam", "otp"],
        "Theft": ["steal", "rob", "theft"],
        "Harassment": ["abuse", "threat", "blackmail"]
    }

    for k, words in keywords.items():
        if case_type == k or any(w in text for w in words):
            score += 20

    score += int(truth * 0.2)
    return min(score, 100)
