import threading
import time
import requests
import logging
import random
import string

CAPTCHA_API_KEY = "YOUR_2CAPTCHA_API_KEY"
API_BASE = "https://discord.com/api/v9"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def solve_captcha(site_key, url, max_retries=20, retry_delay=5):
    logging.info("Submitting captcha for solving...")
    captcha_id_resp = requests.post(
        "http://2captcha.com/in.php",
        data={
            "key": CAPTCHA_API_KEY,
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": url,
            "json": 1
        }
    ).json()

    if captcha_id_resp.get("status") != 1:
        logging.error("Failed to submit captcha for solving: %s", captcha_id_resp.get("request"))
        return None

    captcha_id = captcha_id_resp.get("request")
    logging.info("Captcha submitted, polling for result...")

    for attempt in range(max_retries):
        time.sleep(retry_delay)
        res = requests.get(
            "http://2captcha.com/res.php",
            params={
                "key": CAPTCHA_API_KEY,
                "action": "get",
                "id": captcha_id,
                "json": 1
            }
        ).json()
        if res.get("status") == 1:
            logging.info("Captcha solved.")
            return res.get("request")
        elif res.get("request") == "CAPCHA_NOT_READY":
            logging.info("Captcha not ready, retrying... (%d/%d)", attempt+1, max_retries)
        else:
            logging.error("Error solving captcha: %s", res.get("request"))
            break
    logging.error("Captcha solving timed out.")
    return None

def generate_random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def register_account(email, username, password, captcha_token, date_of_birth="2000-01-01", max_retries=3):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT
    }
    payload = {
        "email": email,
        "username": username,
        "password": password,
        "captcha_key": captcha_token,
        "consent": True,
        "date_of_birth": date_of_birth,
        "gift_code_sku_id": None
    }
    for attempt in range(max_retries):
        try:
            r = requests.post(f"{API_BASE}/auth/register", json=payload, headers=headers)
            if r.status_code == 201:
                token = r.json().get("token")
                logging.info("Registered account successfully: %s", email)
                return token
            else:
                logging.warning("Failed to register account (attempt %d): %d - %s", attempt+1, r.status_code, r.text)
        except Exception as e:
            logging.error("Exception during registration attempt %d: %s", attempt+1, e)
        time.sleep(2)
    logging.error("All registration attempts failed for %s", email)
    return None

def worker(thread_id, tokens_per_thread, delay, date_of_birth="2000-01-01"):
    logging.info("Thread %d started, generating %d tokens.", thread_id, tokens_per_thread)
    site_key = "6Lc_aX0UAAAAABx7u6b6v6b6v6b6v6b6v6b6v6b6"  # Example site key, replace with actual
    url = "https://discord.com/register"
    for i in range(tokens_per_thread):
        logging.info("Thread %d generating token %d/%d", thread_id, i+1, tokens_per_thread)
        email = f"{generate_random_string(6)}@example.com"
        username = generate_random_string(8)
        password = generate_random_string(10)
        captcha_token = solve_captcha(site_key, url)
        if not captcha_token:
            logging.warning("Skipping registration due to captcha failure.")
            continue
        token = register_account(email, username, password, captcha_token, date_of_birth)
        if token:
            with open("tokens.txt", "a") as f:
                f.write(token + "\n")
        time.sleep(delay)
    logging.info("Thread %d finished.", thread_id)

def run():
    num_threads = input("Enter number of threads: ")
    tokens_per_thread = input("Enter number of tokens per thread (1-50): ")
    delay = input("Enter delay between tokens (seconds): ")
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")

    try:
        num_threads = int(num_threads)
        tokens_per_thread = int(tokens_per_thread)
        delay = float(delay)
    except:
        logging.warning("Invalid input, using default values.")
        num_threads = 1
        tokens_per_thread = 1
        delay = 2.0

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i+1, tokens_per_thread, delay, date_of_birth))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    logging.info("Token generation completed.")

if __name__ == "__main__":
    run()
