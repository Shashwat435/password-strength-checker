import re
import hashlib
import requests

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "12345678", "111111", "iloveyou", "admin"
}


def check_pwned(password):
    """
    Checks Have I Been Pwned using k-Anonymity.
    The password never leaves this computer in full — only the first
    5 characters of its SHA-1 hash are sent to the API.
    Returns the number of times the password appeared in breaches (0 if safe).
    """
    # Step 1: hash the password locally with SHA-1
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # Step 2: split into prefix (first 5) and suffix (the rest)
    prefix = sha1[:5]
    suffix = sha1[5:]

    # Step 3: send ONLY the prefix to the API
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"User-Agent": "password-strength-checker"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        # No internet or API down — skip the check gracefully
        return None

    # Step 4: the API returns many suffixes + counts. Look for ours.
    for line in response.text.splitlines():
        returned_suffix, count = line.split(":")
        if returned_suffix == suffix:
            return int(count)

    return 0


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

    # Now the breach check
    print("\nChecking against real-world breaches (Have I Been Pwned)...")
    pwned_count = check_pwned(password)

    if pwned_count is None:
        print(" - Could not reach the breach database (check your internet).")
    elif pwned_count == 0:
        print(" - Good news: this password was NOT found in any known breach.")
    else:
        print(f" - WARNING: this password appeared in {pwned_count:,} known breaches!")
        print("   Even if it looks strong, do not use it.")


if __name__ == "__main__":
    main()