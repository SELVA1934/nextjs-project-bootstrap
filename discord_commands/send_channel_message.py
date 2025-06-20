update import requests
import random

API_BASE = "https://discord.com/api/v9"

def send_channel_message(token, channel_id, message, mention=None, add_random_emojis=False):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    if mention == "everyone":
        message = f"@everyone {message}"
    elif mention == "here":
        message = f"@here {message}"
    elif mention:
        message = f"<@{mention}> {message}"

    try:
        r = requests.post(f"{API_BASE}/channels/{channel_id}/messages", headers=headers, json={"content": message})
        if r.status_code == 200:
            print("Message sent successfully.")
            if add_random_emojis:
                emojis = ["😀", "😂", "😍", "👍", "🎉", "🔥", "😎", "🤖", "💥", "🌟"]
                emoji = random.choice(emojis)
                react_url = f"{API_BASE}/channels/{channel_id}/messages/{r.json()['id']}/reactions/{emoji}/@me"
                react_resp = requests.put(react_url, headers=headers)
                if react_resp.status_code == 204:
                    print(f"Reacted with emoji {emoji}")
                else:
                    print(f"Failed to react with emoji: {react_resp.status_code} - {react_resp.text}")
        else:
            print(f"Failed to send message: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    channel_id = input(f"\033[95mEnter channel ID for token [{token[:6]}...]: \033[0m")
    message = input("\033[95mEnter message content: \033[0m")
    want_mention = input("\033[95mDo you want to mention someone? (yes/no): \033[0m").lower()
    mention = None
    if want_mention == "yes":
        mention = input("\033[95mEnter user ID to mention, or 'everyone'/'here': \033[0m").strip()
    add_emojis_input = input("\033[95mAdd random emoji reaction? (yes/no): \033[0m").lower()
    add_random_emojis = add_emojis_input == "yes"
    send_channel_message(token, channel_id, message, mention if mention else None, add_random_emojis)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

if __name__ == "__main__":
    token = load_token()
    channel_id = input("Enter channel ID: ")
    message = input("Enter message content: ")
    want_mention = input("Do you want to mention someone? (yes/no): ").lower()
    mention = None
    if want_mention == "yes":
        mention = input("Enter user ID to mention, or 'everyone'/'here': ").strip()
    add_emojis_input = input("Add random emoji reaction? (yes/no): ").lower()
    add_random_emojis = add_emojis_input == "yes"
    send_channel_message(token, channel_id, message, mention if mention else None, add_random_emojis)
