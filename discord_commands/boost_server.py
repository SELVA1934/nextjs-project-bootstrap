import requests

def boost_server(token, guild_id, amount, proxy=None):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    success_count = 0
    for _ in range(amount):
        # Attempt to send a POST request to boost the server
        # Note: This endpoint and payload are not officially documented and may not work
        url = f"https://discord.com/api/v9/guilds/{guild_id}/premium/subscription"
        payload = {}
        try:
            r = requests.post(url, headers=headers, json=payload, proxies=proxy)
            if r.status_code == 201:
                success_count += 1
                print(f"\033[92mBoosted server {guild_id} with token [{token[:6]}...] successfully.\033[0m")
            else:
                print(f"\033[91mFailed to boost server {guild_id} with token [{token[:6]}...]: {r.status_code} - {r.text}\033[0m")
        except Exception as e:
            print(f"Error boosting server {guild_id} with token [{token[:6]}...]: {e}")
    print(f"Total successful boosts: {success_count} out of {amount}")

def run_with_token(token):
    guild_id = input(f"\033[95mEnter guild ID to boost for token [{token[:6]}...]: \033[0m")
    amount = input("\033[95mEnter amount of boosts: \033[0m")
    try:
        amount = int(amount)
    except:
        amount = 1
    boost_server(token, guild_id, amount)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    guild_id = input("\033[95mEnter guild ID to boost for all tokens: \033[0m")
    amount = input("\033[95mEnter amount of boosts for all tokens: \033[0m")
    try:
        amount = int(amount)
    except:
        amount = 1
    for token in tokens:
        print(f"Boosting server for token [{token[:6]}...] {amount} times")
        boost_server(token, guild_id, amount)

if __name__ == "__main__":
    run_all_tokens()
