import requests
import urllib.parse

API_BASE = "https://discord.com/api/v9"

def react_to_message(token, channel_id, message_id, emoji):
    headers = {
        "Authorization": token
    }
    # Encode emoji for URL
    emoji_encoded = urllib.parse.quote(emoji)
    try:
        r = requests.put(f"{API_BASE}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me", headers=headers)
        if r.status_code == 204:
            print("Reacted to message successfully.")
        else:
            print(f"Failed to react to message: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error reacting to message: {e}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    channel_id = input(f"\033[95mEnter channel ID for token [{token[:6]}...]: \033[0m")
    message_id = input("\033[95mEnter message ID: \033[0m")
    emoji = input("\033[95mEnter emoji (unicode or custom): \033[0m")
    react_to_message(token, channel_id, message_id, emoji)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    channel_id = input("\033[95mEnter channel ID for all tokens: \033[0m")
    message_id = input("\033[95mEnter message ID for all tokens: \033[0m")
    emoji = input("\033[95mEnter emoji (unicode or custom) for all tokens: \033[0m")
    for token in tokens:
        print(f"Reacting to message for token [{token[:6]}...]")
        react_to_message(token, channel_id, message_id, emoji)

if __name__ == "__main__":
    run_all_tokens()
