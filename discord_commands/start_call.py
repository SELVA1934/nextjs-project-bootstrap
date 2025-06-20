import requests

API_BASE = "https://discord.com/api/v9"

def start_call(token, user_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    # Create DM channel with user
    payload = {
        "recipient_id": user_id
    }
    r = requests.post(f"{API_BASE}/users/@me/channels", headers=headers, json=payload)
    if r.status_code != 200:
        print(f"\033[91mFailed to create DM channel: {r.status_code} - {r.text}\033[0m")
        return
    channel_id = r.json()["id"]

    # Mock starting call - Discord API does not provide direct call start endpoint for user tokens
    print(f"\033[92mCall started with user ID {user_id} in DM channel {channel_id} (mock implementation).\033[0m")

def run_with_token(token):
    user_id = input(f"\033[95mEnter user ID to start call for token [{token[:6]}...]: \033[0m")
    start_call(token, user_id)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    user_id = input("\033[95mEnter user ID to start call for all tokens: \033[0m")
    for token in tokens:
        print(f"Starting call for token [{token[:6]}...]")
        start_call(token, user_id)

if __name__ == "__main__":
    run_all_tokens()
