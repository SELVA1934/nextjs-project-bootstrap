import requests

API_BASE = "https://discord.com/api/v9"

def accept_rules(token, guild_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    # Get channels in the guild
    channels_resp = requests.get(f"{API_BASE}/guilds/{guild_id}/channels", headers=headers)
    if channels_resp.status_code != 200:
        print(f"Failed to get channels for guild {guild_id}: {channels_resp.status_code} - {channels_resp.text}")
        return
    channels = channels_resp.json()
    # Find rules channel (usually named 'rules' or with type 4 (category) or 5 (announcement))
    rules_channel = None
    for channel in channels:
        if channel['name'].lower() == 'rules' or channel['type'] == 4 or channel['type'] == 5:
            rules_channel = channel
            break
    if not rules_channel:
        print(f"Rules channel not found in guild {guild_id}")
        return
    # Get messages in rules channel
    messages_resp = requests.get(f"{API_BASE}/channels/{rules_channel['id']}/messages", headers=headers)
    if messages_resp.status_code != 200:
        print(f"Failed to get messages in rules channel {rules_channel['id']}: {messages_resp.status_code} - {messages_resp.text}")
        return
    messages = messages_resp.json()
    if not messages:
        print(f"No messages found in rules channel {rules_channel['id']}")
        return
    # React to the first message with a checkmark emoji
    message_id = messages[0]['id']
    emoji = "%E2%9C%85"  # Unicode for white check mark
    react_resp = requests.put(f"{API_BASE}/channels/{rules_channel['id']}/messages/{message_id}/reactions/{emoji}/@me", headers=headers)
    if react_resp.status_code == 204:
        print(f"\033[92mAccepted rules for guild {guild_id} with token [{token[:6]}...].\033[0m")
    else:
        print(f"Failed to react to rules message: {react_resp.status_code} - {react_resp.text}")

def run_with_token(token):
    guild_id = input(f"\033[95mEnter guild ID to accept rules for token [{token[:6]}...]: \033[0m")
    accept_rules(token, guild_id)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    guild_id = input("\033[95mEnter guild ID to accept rules for all tokens: \033[0m")
    for token in tokens:
        print(f"Accepting rules for guild {guild_id} with token [{token[:6]}...]")
        accept_rules(token, guild_id)

if __name__ == "__main__":
    run_all_tokens()
