import requests

API_BASE = "https://discord.com/api/v9"

def change_custom_status(token, text, emoji_name=None, emoji_id=None, proxy=None):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    custom_status = {
        "text": text
    }
    if emoji_name:
        custom_status["emoji_name"] = emoji_name
    if emoji_id:
        custom_status["emoji_id"] = emoji_id

    payload = {
        "custom_status": custom_status
    }

    r = requests.patch(f"{API_BASE}/users/@me/settings", headers=headers, json=payload, proxies=proxy)
    if r.status_code == 200:
        print("Custom status changed successfully.")
    else:
        print(f"Failed to change custom status: {r.status_code} - {r.text}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    text = input(f"\033[95mEnter custom status text for token [{token[:6]}...]: \033[0m")
    emoji_name = input("\033[95mEnter emoji name (optional): \033[0m")
    emoji_id = input("\033[95mEnter emoji ID (optional): \033[0m")
    change_custom_status(token, text, emoji_name or None, emoji_id or None)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    text = input("\033[95mEnter custom status text for all tokens: \033[0m")
    emoji_name = input("\033[95mEnter emoji name (optional): \033[0m")
    emoji_id = input("\033[95mEnter emoji ID (optional): \033[0m")
    for token in tokens:
        print(f"Changing custom status for token [{token[:6]}...]")
        change_custom_status(token, text, emoji_name or None, emoji_id or None)

if __name__ == "__main__":
    run_all_tokens()
