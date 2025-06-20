import requests

API_BASE = "https://discord.com/api/v9"

def send_dm(token, recipient_id, message):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    # Create DM channel
    payload = {
        "recipient_id": recipient_id
    }
    try:
        r = requests.post(f"{API_BASE}/users/@me/channels", headers=headers, json=payload)
        if r.status_code != 200:
            print(f"Failed to create DM channel: {r.status_code} - {r.text}")
            return
        channel_id = r.json()["id"]

        # Send message
        payload = {
            "content": message
        }
        r = requests.post(f"{API_BASE}/channels/{channel_id}/messages", headers=headers, json=payload)
        if r.status_code == 200:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error sending DM: {e}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    recipient_id = input(f"\033[95mEnter recipient user ID for token [{token[:6]}...]: \033[0m")
    message = input("\033[95mEnter message to send: \033[0m")
    send_dm(token, recipient_id, message)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

if __name__ == "__main__":
    token = load_token()
    recipient_id = input("Enter recipient user ID: ")
    message = input("Enter message to send: ")
    send_dm(token, recipient_id, message)
