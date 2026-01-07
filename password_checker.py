pwd = input("Enter password: ")

score = 0
if len(pwd) >= 8: score += 1
if any(c.isdigit() for c in pwd): score += 1
if any(c.isupper() for c in pwd): score += 1
if any(c in "!@#$%^&*" for c in pwd): score += 1

print("Strength:", ["Weak", "Medium", "Strong", "Very Strong"][score-1])
