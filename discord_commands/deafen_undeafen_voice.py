import requests

API_BASE = "https://discord.com/api/v9"

def deafen_undeafen(token, guild_id, deafen=True, proxy=None):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "self_deaf": deafen
    }
    try:
        r = requests.patch(f"{API_BASE}/users/@me/guilds/{guild_id}/voice-states/@me", headers=headers, json=payload, proxies=proxy)
        if r.status_code == 204:
            print(f"{'Deafened' if deafen else 'Undeafened'} successfully.")
        else:
            print(f"Failed to {'deafen' if deafen else 'undeafen'}: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error during {'deafen' if deafen else 'undeafen'} request: {e}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    guild_id = input(f"\033[95mEnter guild ID for token [{token[:6]}...]: \033[0m")
    action = input("\033[95mEnter action (deafen/undeafen): \033[0m").lower()
    if action == "deafen":
        deafen_undeafen(token, guild_id, True)
    elif action == "undeafen":
        deafen_undeafen(token, guild_id, False)
    else:
        print("\033[93mInvalid action.\033[0m")
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens(proxy=None):
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    guild_id = input("\033[95mEnter guild ID for all tokens: \033[0m")
    action = input("\033[95mEnter action (deafen/undeafen) for all tokens: \033[0m").lower()
    for token in tokens:
        if action == "deafen":
            print(f"Deafening for token [{token[:6]}...]")
            deafen_undeafen(token, guild_id, True, proxy)
        elif action == "undeafen":
            print(f"Undeafening for token [{token[:6]}...]")
            deafen_undeafen(token, guild_id, False, proxy)
        else:
            print("\033[93mInvalid action.\033[0m")
            break

if __name__ == "__main__":
    run_all_tokens()
