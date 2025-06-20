import requests

API_BASE = "https://discord.com/api/v9"

def ping_everyone_invite(token, channel_id, invite_link, proxy=None):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    message_content = f"@everyone Join the server: {invite_link}"
    payload = {
        "content": message_content,
        "allowed_mentions": {
            "parse": ["everyone"]
        }
    }
    try:
        r = requests.post(f"{API_BASE}/channels/{channel_id}/messages", headers=headers, json=payload, proxies=proxy)
        if r.status_code == 200 or r.status_code == 201:
            print(f"\033[92mPinged everyone in channel {channel_id} with invite link.\033[0m")
        else:
            print(f"\033[91mFailed to send message: {r.status_code} - {r.text}\033[0m")
    except Exception as e:
        print(f"Error sending message: {e}")

def run_with_token(token):
    channel_id = input(f"\033[95mEnter channel ID for token [{token[:6]}...]: \033[0m")
    invite_link = input("\033[95mEnter Discord invite link: \033[0m")
    ping_everyone_invite(token, channel_id, invite_link)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens(proxy=None):
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    channel_id = input("\033[95mEnter channel ID for all tokens: \033[0m")
    invite_link = input("\033[95mEnter Discord invite link for all tokens: \033[0m")
    for token in tokens:
        print(f"Pinging everyone for token [{token[:6]}...]")
        ping_everyone_invite(token, channel_id, invite_link, proxy)

if __name__ == "__main__":
    run_all_tokens()
