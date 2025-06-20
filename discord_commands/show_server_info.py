import requests

API_BASE = "https://discord.com/api/v9"

def show_server_info(token, guild_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    try:
        r = requests.get(f"{API_BASE}/guilds/{guild_id}", headers=headers)
        if r.status_code == 200:
            data = r.json()
            print(f"\033[92mServer Info for guild {guild_id}:\033[0m")
            print(f"Name: {data.get('name')}")
            print(f"ID: {data.get('id')}")
            print(f"Owner ID: {data.get('owner_id')}")
            print(f"Member Count: {data.get('approximate_member_count', 'N/A')}")
            print(f"Description: {data.get('description', 'N/A')}")
        else:
            print(f"\033[91mFailed to fetch server info: {r.status_code} - {r.text}\033[0m")
    except Exception as e:
        print(f"Error fetching server info: {e}")

def run_with_token(token):
    guild_id = input(f"\033[95mEnter guild ID to show info for token [{token[:6]}...]: \033[0m")
    show_server_info(token, guild_id)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    guild_id = input("\033[95mEnter guild ID to show info for all tokens: \033[0m")
    for token in tokens:
        print(f"Showing server info for token [{token[:6]}...]")
        show_server_info(token, guild_id)

if __name__ == "__main__":
    run_all_tokens()
