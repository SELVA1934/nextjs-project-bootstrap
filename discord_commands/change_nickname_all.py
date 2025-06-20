import requests

API_BASE = "https://discord.com/api/v9"

def change_nickname(token, guild_id, new_nickname, proxy=None):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "nick": new_nickname
    }
    try:
        r = requests.patch(f"{API_BASE}/guilds/{guild_id}/members/@me", headers=headers, json=payload, proxies=proxy)
        if r.status_code == 200:
            return True
        else:
            print(f"Failed to change nickname in guild {guild_id}: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"Error changing nickname in guild {guild_id}: {e}")
        return False

def get_guilds(token, proxy=None):
    headers = {
        "Authorization": token
    }
    r = requests.get(f"{API_BASE}/users/@me/guilds", headers=headers, proxies=proxy)
    if r.status_code == 200:
        return r.json()
    else:
        return []

def change_nickname_all(token, new_nickname, proxy=None):
    guilds = get_guilds(token, proxy)
    success_count = 0
    for guild in guilds:
        guild_id = guild["id"]
        if change_nickname(token, guild_id, new_nickname, proxy):
            print(f"Changed nickname in guild {guild['name']}")
            success_count += 1
        else:
            print(f"Failed to change nickname in guild {guild['name']}")
    print(f"Nickname changed in {success_count} guilds.")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    new_nickname = input(f"\033[95mEnter new nickname for token [{token[:6]}...]: \033[0m")
    change_nickname_all(token, new_nickname)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens(proxy=None):
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    new_nickname = input("\033[95mEnter new nickname for all tokens: \033[0m")
    for token in tokens:
        print(f"Changing nickname for token [{token[:6]}...]")
        change_nickname_all(token, new_nickname, proxy)

if __name__ == "__main__":
    run_all_tokens()
