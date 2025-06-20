import requests

API_BASE = "https://discord.com/api/v9"

def bypass_onboarding(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    # Attempt to mark onboarding as complete by updating user settings
    payload = {
        "tutorial_flags": 0  # Clear tutorial flags to mark onboarding complete
    }
    try:
        r = requests.patch(f"{API_BASE}/users/@me/settings", headers=headers, json=payload)
        if r.status_code == 200:
            print(f"\033[92mBypassed onboarding for token [{token[:6]}...].\033[0m")
        else:
            print(f"Failed to bypass onboarding: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error bypassing onboarding for token [{token[:6]}...]: {e}")

def run_with_token(token):
    bypass_onboarding(token)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    for token in tokens:
        print(f"Bypassing onboarding for token [{token[:6]}...]")
        bypass_onboarding(token)

if __name__ == "__main__":
    run_all_tokens()
