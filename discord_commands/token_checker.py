import requests

API_BASE = "https://discord.com/api/v9"

def check_token(token):
    headers = {
        "Authorization": token
    }
    r = requests.get(f"{API_BASE}/users/@me", headers=headers)
    if r.status_code == 200:
        user = r.json()
        print(f"\033[92mToken is valid: {token} - User: {user['username']}#{user['discriminator']}\033[0m")
        return True
    else:
        print(f"\033[91mInvalid token: {token} - {r.status_code} - {r.text}\033[0m")
        return False

def run_with_token(token):
    print(f"Checking token [{token[:6]}...]")
    check_token(token)
    choice = input("[ 0 ] Back: ").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    valid_tokens = []
    for token in tokens:
        print(f"Checking token [{token[:6]}...]")
        if check_token(token):
            valid_tokens.append(token)
    # Rewrite tokens.txt with only valid tokens
    with open("tokens.txt", "w") as f:
        for vt in valid_tokens:
            f.write(vt + "\n")

if __name__ == "__main__":
    run_all_tokens()
