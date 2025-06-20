import requests

API_BASE = "https://discord.com/api/v9"

def send_friend_request(token, user_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "username": None,
        "discriminator": None,
        "user_id": user_id
    }
    try:
        r = requests.post(f"{API_BASE}/users/@me/relationships", headers=headers, json=payload)
        if r.status_code == 204:
            print(f"\033[92mFriend request sent successfully to user ID {user_id}.\033[0m")
        else:
            print(f"\033[91mFailed to send friend request: {r.status_code} - {r.text}\033[0m")
    except Exception as e:
        print(f"Error sending friend request: {e}")

def run_with_token(token):
    user_id = input(f"\033[95mEnter user ID to send friend request for token [{token[:6]}...]: \033[0m")
    send_friend_request(token, user_id)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    user_id = input("\033[95mEnter user ID to send friend request for all tokens: \033[0m")
    for token in tokens:
        print(f"Sending friend request for token [{token[:6]}...]")
        send_friend_request(token, user_id)

if __name__ == "__main__":
    run_all_tokens()
