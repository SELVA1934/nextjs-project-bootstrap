import requests

API_BASE = "https://discord.com/api/v9"

def token_login(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    r = requests.get(f"{API_BASE}/users/@me", headers=headers)
    if r.status_code == 200:
        user = r.json()
        print(f"\033[92mToken login successful for user: {user.get('username')}#{user.get('discriminator')} [{user.get('id')}]\033[0m")
    else:
        print(f"\033[91mToken login failed: {r.status_code} - {r.text}\033[0m")

def run_with_token(token):
    token_login(token)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    for token in tokens:
        print(f"Logging in token [{token[:6]}...]")
        token_login(token)

if __name__ == "__main__":
    run_all_tokens()
