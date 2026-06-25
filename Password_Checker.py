import re

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "12345678", "111111", "iloveyou", "admin"
}

def check_password(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Make it at least 8 characters (12+ is much better).")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add some lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add some uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add some numbers.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        feedback.append("Add a special character like ! @ # $.")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback = ["This is one of the most common passwords ever. Never use it."]

    if score <= 2:
        verdict = "Weak"
    elif score <= 4:
        verdict = "Medium"
    else:
        verdict = "Strong"

    return verdict, score, feedback


def main():
    print("=== Password Strength Checker ===")
    password = input("Enter a password to check: ")
    verdict, score, feedback = check_password(password)

    print(f"\nStrength: {verdict} (score {score}/6)")
    if feedback:
        print("\nSuggestions to improve:")
        for tip in feedback:
            print(f" - {tip}")
    else:
        print("Great password!")


if __name__ == "__main__":
    main()