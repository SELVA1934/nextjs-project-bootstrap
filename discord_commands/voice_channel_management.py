import requests

API_BASE = "https://discord.com/api/v9"

def get_current_voice_state(token, guild_id):
    headers = {
        "Authorization": token
    }
    r = requests.get(f"{API_BASE}/users/@me/guilds/{guild_id}/voice-states/@me", headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return None

def move_to_voice_channel(token, guild_id, channel_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "channel_id": channel_id,
        "self_mute": False,
        "self_deaf": False
    }
    r = requests.patch(f"{API_BASE}/users/@me/guilds/{guild_id}/voice-states/@me", headers=headers, json=payload)
    if r.status_code == 204:
        print("Moved to voice channel successfully.")
    else:
        print(f"Failed to move to voice channel: {r.status_code} - {r.text}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    guild_id = input(f"\033[95mEnter guild ID for token [{token[:6]}...]: \033[0m")
    channel_id = input("\033[95mEnter voice channel ID to move to: \033[0m")
    move_to_voice_channel(token, guild_id, channel_id)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    guild_id = input("\033[95mEnter guild ID for all tokens: \033[0m")
    channel_id = input("\033[95mEnter voice channel ID to move to for all tokens: \033[0m")
    for token in tokens:
        print(f"Moving to voice channel for token [{token[:6]}...]")
        move_to_voice_channel(token, guild_id, channel_id)

if __name__ == "__main__":
    run_all_tokens()
