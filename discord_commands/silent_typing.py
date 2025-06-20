import requests
import time

API_BASE = "https://discord.com/api/v9"

def silent_typing(token, channel_id, duration=5):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    # Send typing indicator repeatedly for duration seconds
    end_time = time.time() + duration
    while time.time() < end_time:
        r = requests.post(f"{API_BASE}/channels/{channel_id}/typing", headers=headers)
        if r.status_code != 204:
            print(f"\033[91mFailed to send typing indicator: {r.status_code} - {r.text}\033[0m")
            break
        time.sleep(3)  # Discord typing indicator lasts ~10 seconds, send every 3 seconds to keep alive
    print(f"\033[92mSilent typing completed in channel {channel_id}.\033[0m")

def run_with_token(token):
    channel_id = input(f"\033[95mEnter channel ID for token [{token[:6]}...]: \033[0m")
    duration = input("\033[95mEnter typing duration in seconds (default 5): \033[0m")
    try:
        duration = int(duration)
    except:
        duration = 5
    silent_typing(token, channel_id, duration)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    channel_id = input("\033[95mEnter channel ID for all tokens: \033[0m")
    duration = input("\033[95mEnter typing duration in seconds (default 5): \033[0m")
    try:
        duration = int(duration)
    except:
        duration = 5
    for token in tokens:
        print(f"Sending silent typing for token [{token[:6]}...]")
        silent_typing(token, channel_id, duration)

if __name__ == "__main__":
    run_all_tokens()
