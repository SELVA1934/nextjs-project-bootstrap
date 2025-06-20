import requests

API_BASE = "https://discord.com/api/v9"

def edit_message(token, channel_id, message_id, new_content, proxy=None):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "content": new_content
    }
    try:
        r = requests.patch(f"{API_BASE}/channels/{channel_id}/messages/{message_id}", headers=headers, json=payload, proxies=proxy)
        if r.status_code == 200:
            print("Message edited successfully.")
        else:
            print(f"Failed to edit message: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error editing message: {e}")

def delete_message(token, channel_id, message_id, proxy=None):
    headers = {
        "Authorization": token
    }
    try:
        r = requests.delete(f"{API_BASE}/channels/{channel_id}/messages/{message_id}", headers=headers, proxies=proxy)
        if r.status_code == 204:
            print("Message deleted successfully.")
        else:
            print(f"Failed to delete message: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error deleting message: {e}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    action = input(f"\033[95mEnter action (edit/delete) for token [{token[:6]}...]: \033[0m").lower()
    channel_id = input("\033[95mEnter channel ID: \033[0m")
    message_id = input("\033[95mEnter message ID: \033[0m")
    if action == "edit":
        new_content = input("\033[95mEnter new message content: \033[0m")
        edit_message(token, channel_id, message_id, new_content)
    elif action == "delete":
        delete_message(token, channel_id, message_id)
    else:
        print("\033[93mInvalid action.\033[0m")
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens(proxy=None):
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    action = input("\033[95mEnter action (edit/delete) for all tokens: \033[0m").lower()
    channel_id = input("\033[95mEnter channel ID: \033[0m")
    message_id = input("\033[95mEnter message ID: \033[0m")
    if action == "edit":
        new_content = input("\033[95mEnter new message content: \033[0m")
        for token in tokens:
            print(f"Editing message for token [{token[:6]}...]")
            edit_message(token, channel_id, message_id, new_content, proxy)
    elif action == "delete":
        for token in tokens:
            print(f"Deleting message for token [{token[:6]}...]")
            delete_message(token, channel_id, message_id, proxy)
    else:
        print("\033[93mInvalid action.\033[0m")

if __name__ == "__main__":
    run_all_tokens()
