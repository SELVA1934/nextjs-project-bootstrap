import random
import string

def generate_token(length=59):
    # Generate a mock Discord token-like string
    chars = string.ascii_letters + string.digits + ".-_"
    return ''.join(random.choice(chars) for _ in range(length))

def run():
    count = input("Enter number of tokens to generate: ")
    try:
        count = int(count)
    except:
        count = 1
    tokens = [generate_token() for _ in range(count)]
    with open("tokens.txt", "w") as f:
        for token in tokens:
            f.write(token + "\n")
    print(f"Generated {count} tokens and saved to tokens.txt")

if __name__ == "__main__":
    run()
