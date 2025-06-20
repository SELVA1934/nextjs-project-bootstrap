def report_user(token, user_id, reason):
    # Reporting users is not supported via Discord public API
    print(f"\033[93mReporting users is not supported via Discord API. Cannot report user ID {user_id}.\033[0m")

def run_with_token(token):
    user_id = input(f"\033[95mEnter user ID to report for token [{token[:6]}...]: \033[0m")
    reason = input("\033[95mEnter reason for reporting: \033[0m")
    report_user(token, user_id, reason)
    choice = input("\033[95m[ 0 ] Back: \033[0m").strip()
    if choice == '0':
        return

def run_all_tokens():
    with open("tokens.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    user_id = input("\033[95mEnter user ID to report for all tokens: \033[0m")
    reason = input("\033[95mEnter reason for reporting: \033[0m")
    for token in tokens:
        print(f"Reporting user for token [{token[:6]}...]")
        report_user(token, user_id, reason)

if __name__ == "__main__":
    run_all_tokens()
