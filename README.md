# Password Strength Checker

A command-line tool that rates how strong a password is, AND checks whether
it has appeared in real-world data breaches using the Have I Been Pwned API.

## Features
- Rates password strength: Weak / Medium / Strong
- Checks length, uppercase, lowercase, numbers, and special characters
- Flags commonly-used weak passwords
- Checks the password against billions of real breached passwords via
  the Have I Been Pwned API

## How the breach check stays private (k-Anonymity)
The password is hashed locally on your machine using SHA-1. Only the first
5 characters of that hash are sent to the API. The full password and full
hash never leave your computer, so your password stays private while still
being checked against known breaches.

## How to run
1. Make sure Python 3 is installed.
2. Install the one dependency:
   pip3 install requests
3. Run the script:
   python3 Password_Checker.py
4. Enter a password when prompted.

## Note
Built for educational purposes as part of learning security fundamentals.