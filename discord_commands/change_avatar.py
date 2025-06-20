import requests
import base64

API_BASE = "https://discord.com/api/v9"

def change_avatar(token, image_path):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Image file not found: {image_path}")
        return
    except Exception as e:
        print(f"Error reading image file: {e}")
        return
    if not image_path.lower().endswith('.png'):
        print("Warning: Image is not a PNG file. Discord may reject the avatar.")
    payload = {
        "avatar": f"data:image/png;base64,{encoded_string}"
    }
    try:
        r = requests.patch(f"{API_BASE}/users/@me", headers=headers, json=payload)
        if r.status_code == 200:
            print("Avatar changed successfully.")
        else:
            print(f"Failed to change avatar: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error changing avatar: {e}")

def load_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

def run_with_token(token):
    image_path = input(f"\033[95mEnter path to avatar image (PNG) for token [{token[:6]}...]: \033[0m")
    change_avatar(token, image_path)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    image_path = input("\033[95mEnter path to avatar image (PNG) for all tokens: \033[0m")
    for token in tokens:
        print(f"Changing avatar for token [{token[:6]}...]")
        change_avatar(token, image_path)

if __name__ == "__main__":
    run_all_tokens()

if __name__ == "__main__":
    run_all_tokens()
