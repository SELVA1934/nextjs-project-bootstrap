import sys
import importlib
import threading
import os

def load_tokens():
    with open("tokens.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

COMMANDS = {
    "1": ("Change Status", "discord_commands.change_status"),
    "2": ("Change Bio", "discord_commands.update_bio"),
    "3": ("DM Spammer", "discord_commands.send_dm"),
    "4": ("Edit/Delete Msg", "discord_commands.edit_delete_message"),
    "5": ("Change Avatar", "discord_commands.change_avatar"),
    "6": ("Leaver", "discord_commands.leave_server"),
    "7": ("Change Nickname", "discord_commands.change_nickname_all"),
    "8": ("Joiner", "discord_commands.join_server_invite"),
    "9": ("Join Voice", "discord_commands.voice_channel_management"),
    "10": ("Join/Leave Group", "discord_commands.join_leave_group_dm"),
    "11": ("React to Msg", "discord_commands.react_message"),
    "12": ("Change Status", "discord_commands.change_custom_status"),
    "13": ("Mute/Unmute", "discord_commands.mute_unmute_voice"),
    "14": ("Deafen/Undeafen", "discord_commands.deafen_undeafen_voice"),
    "15": ("Spammer ", "discord_commands.send_channel_message"),
    "16": ("Token Checker", "discord_commands.token_checker"),
    "17": ("Friend Spammer ", "discord_commands.send_friend_request"),
    "18": ("Call Spammer ", "discord_commands.start_call"),
    "19": ("Report Spam ", "discord_commands.report_user"),
    "20": ("Silent Typing", "discord_commands.silent_typing"),
    "21": ("Accept Rules", "discord_commands.accept_rules"),
    "22": ("Server Info", "discord_commands.show_server_info"),
    "23": ("Bypass Onboarding", "discord_commands.bypass_onboarding"),
    "24": ("Pinger ", "discord_commands.ping_everyone_invite"),
    "25": ("Token Login", "discord_commands.token_login"),
    "26": ("Soundboard Spam ", "discord_commands.random_soundboard"),
    "27": ("Boost Server", "discord_commands.boost_server"),
}

def run_command_for_token(module, token):
    if hasattr(module, "run_with_token"):
        module.run_with_token(token)
    elif hasattr(module, "main"):
        # fallback to main, but main should be updated to accept token param ideally
        module.main()
    else:
        print(f"Module {module} has no runnable entry point.")

def print_banner():
    banner = (
        "\033[95m ____  _               _                 _   _                 _ \033[0m\n"
        "\033[91m|  _ \\| |__   ___  ___| | _____ _ __ ___| | | | ___   ___   __| |\033[0m\n"
        "\033[93m| | | | '_ \\ / _ \\/ __| |/ / _ \\ '__/ __| |_| |/ _ \\ / _ \\ / _` |\033[0m\n"
        "\033[92m| |_| | | | |  __/ (__|   <  __/ |  \\__ \\  _  | (_) | (_) | (_| |\033[0m\n"
        "\033[94m|____/|_| |_|\\___|\\___|_|\\_\\___|_|  |___/_| |_|\\___/ \\___/ \\__,_|\033[0m\n"
        "                                                                 "
    )
    lines = banner.split('\n')
    width = 80
    for line in lines:
        print(line.center(width))
    print("\nDiscord User Token Control Tool Dashboard")
    print("Select a command to run:")

def print_commands():
    keys = list(COMMANDS.keys())
    row_size = 3
    colors = ["\033[95m", "\033[91m", "\033[93m"]  # magenta, red, yellow
    reset = "\033[0m"
    for i in range(0, len(keys), row_size):
        row_keys = keys[i:i+row_size]
        row_str = ""
        for idx, key in enumerate(row_keys):
            color = colors[idx % len(colors)]
            desc = COMMANDS[key][0]
            row_str += f"{color}{key}. {desc}{reset}".ljust(40)
        print(row_str)
    print("0. Exit")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    tokens = load_tokens()
    clear_screen()
    print_banner()
    print_commands()

    while True:
        choice = input("Enter choice: ").strip()
        if choice == "0":
            print("Exiting.")
            sys.exit(0)
        elif choice in COMMANDS:
            clear_screen()
            print_banner()
            print_commands()
            module_name = COMMANDS[choice][1]
            try:
                module = importlib.import_module(module_name)
                print(f"Running command '{COMMANDS[choice][0]}' for all tokens concurrently...")
                threads = []
                for token in tokens:
                    t = threading.Thread(target=run_command_for_token, args=(module, token))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                print("All commands completed.")
                input("Press Enter to return to the dashboard...")
                clear_screen()
                print_banner()
                print_commands()
            except Exception as e:
                print(f"Error running command: {e}")
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
