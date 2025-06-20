import requests

API_BASE = "https://discord.com/api/v9"

def leave_server(token, guild_id, proxy=None):
    headers = {
        "Authorization": token
    }
    try:
        r = requests.delete(f"{API_BASE}/users/@me/guilds/{guild_id}", headers=headers, proxies=proxy)
        if r.status_code == 204:
            print("Left the server successfully.")
        else:
            print(f"Failed to leave server: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error leaving server: {e}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    guild_id = input(f"\033[95mEnter the server (guild) ID to leave for token [{token[:6]}...]: \033[0m")
    leave_server(token, guild_id)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens(proxy=None):
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    guild_id = input("\033[95mEnter the server (guild) ID to leave for all tokens: \033[0m")
    for token in tokens:
        print(f"Leaving server for token [{token[:6]}...]")
        leave_server(token, guild_id, proxy)

if __name__ == "__main__":
    run_all_tokens()
