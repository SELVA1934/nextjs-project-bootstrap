import requests

API_BASE = "https://discord.com/api/v9"

def join_server(token, invite_code, proxy=None):
    headers = {
        "Authorization": token
    }
    try:
        r = requests.post(f"{API_BASE}/invites/{invite_code}", headers=headers, proxies=proxy)
        if r.status_code == 200:
            print("Joined server successfully.")
        else:
            print(f"Failed to join server: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error joining server: {e}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    invite_code = input(f"\033[95mEnter server invite code for token [{token[:6]}...]: \033[0m")
    join_server(token, invite_code)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens(proxy=None):
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    invite_code = input("\033[95mEnter server invite code for all tokens: \033[0m")
    for token in tokens:
        print(f"Joining server for token [{token[:6]}...]")
        join_server(token, invite_code, proxy)

if __name__ == "__main__":
    run_all_tokens()
