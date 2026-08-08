import requests
import json
import os
import time
import random
from colorama import init, Fore, Style

init(autoreset=True)

# === CONFIGURATION ===
API_BASE = "https://rocket-trace-bot.vercel.app/api?num="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) Gecko/117.0 Firefox/117.0",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://rocket-xd.vercel.app/",
    "Connection": "keep-alive"
}

# === Typing Animation (prints each char with delay) ===
def type_effect(text, delay=0.002):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# === Print with typing effect line by line ===
def type_print_lines(text, delay=0.002):
    for line in text.splitlines():
        type_effect(line, delay)

# === Banner ===
def show_banner():
    os.system("clear")
    ascii_banner = r"""{Fore.GREEN}

____   ___   ____ _  __ _____ _____ 
|  _ \ / _ \ / ___| |/ /| ____|_   _|
| |_) | | | | |   | ' / |  _|   | |  
|  _ <| |_| | |___| . \ | |___  | |  
|_| \_\\___/ \____|_|\_\|_____| |_|

🚀 ROCKET xD NUMBER LOOKUP 🚀
"""
    credit = f"{Fore.RED}{Style.BRIGHT}➤ Made by Rocket xD\n"
    type_effect(ascii_banner, delay=0.0005)
    print(credit)

# === Extract JSON from raw text (handles both arrays and objects) ===
def extract_json(raw_text):
    # Try to parse the whole thing first
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    # Find the first '{' or '[' (whichever comes first)
    start_obj = raw_text.find('{')
    start_arr = raw_text.find('[')
    if start_obj == -1 and start_arr == -1:
        raise ValueError("No JSON object or array found in response")

    # Choose the earliest start
    if start_obj == -1:
        start = start_arr
        open_char = '['
        close_char = ']'
    elif start_arr == -1:
        start = start_obj
        open_char = '{'
        close_char = '}'
    else:
        if start_obj < start_arr:
            start = start_obj
            open_char = '{'
            close_char = '}'
        else:
            start = start_arr
            open_char = '['
            close_char = ']'

    # Find the matching closing bracket/brace using a stack
    stack = []
    i = start
    while i < len(raw_text):
        ch = raw_text[i]
        if ch == open_char:
            stack.append(ch)
        elif ch == close_char:
            if stack:
                stack.pop()
                if not stack:
                    # Found the matching close
                    end = i + 1
                    json_str = raw_text[start:end]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        raise ValueError("Extracted JSON is invalid")
        i += 1
    raise ValueError("No matching closing bracket/brace found")

# === Pretty Print a Single Record (with typing animation) ===
def pretty_print_record(record, index):
    """Display a single result with a clear header and formatted fields."""
    lines = []
    lines.append(Fore.LIGHTRED_EX + f"\n{'='*50}")
    lines.append(Fore.LIGHTRED_EX + f" Result #{index} ")
    lines.append(Fore.LIGHTRED_EX + f"{'='*50}\n")

    if isinstance(record, dict):
        for key, value in record.items():
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, indent=2, ensure_ascii=False)
                value_str = "\n".join("    " + line for line in value_str.splitlines())
                lines.append(Fore.CYAN + f"{key}:")
                lines.append(Fore.WHITE + value_str)
            else:
                lines.append(Fore.YELLOW + f"{key}: " + Fore.WHITE + f"{value}")
    else:
        lines.append(Fore.WHITE + str(record))

    lines.append(Fore.LIGHTRED_EX + f"{'='*50}\n")

    # Print each line with typing effect
    for line in lines:
        type_effect(line, delay=0.001)

# === Normalize API response into list of dicts ===
def normalize_response(data):
    """
    Accepts the parsed JSON data and returns a list of record-dicts to display.
    """
    if isinstance(data, dict) and "data" in data and data["data"]:
        if isinstance(data["data"], list):
            return data["data"]
        if isinstance(data["data"], dict):
            return [data["data"]]

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        likely_keys = {"name", "title", "mobile", "number", "operator", "circle", "state", "sim"}
        if likely_keys.intersection(set(data.keys())):
            return [data]
        for k, v in data.items():
            if isinstance(v, list) and v:
                return v
            if isinstance(v, dict) and v:
                return [v]

    return []

# === Search Function (API) ===
def search_number(number):
    url = f"{API_BASE}{number}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        raw_text = response.text.strip()

        if response.status_code != 200:
            print(Fore.RED + f"⚠️ HTTP Error {response.status_code}")
            print(Fore.YELLOW + f"Raw response: {raw_text[:200]}...")
            return

        # Extract JSON robustly
        try:
            data = extract_json(raw_text)
        except ValueError as e:
            print(Fore.RED + f"⚠️ Failed to extract JSON: {e}")
            print(Fore.YELLOW + f"Raw response preview: {raw_text[:300]}...")
            return

        records = normalize_response(data)

        if not records:
            print(Fore.YELLOW + "⚠️ No results found.")
            # Optionally show the entire data for debugging
            # print(Fore.CYAN + json.dumps(data, indent=2))
            return

        # Show results with typing animation
        type_print_lines(Fore.CYAN + f"\n📊 Search Results for {number}\n", delay=0.001)

        for idx, user in enumerate(records, 1):
            pretty_print_record(user, idx)

        # Footer with typing effect
        footer = Fore.RED + "\n⚡ Made by Rocket xD\n" + Fore.BLUE + "👉 Join: https://t.me/rocket_xd777\n"
        type_effect(footer, delay=0.001)

    except requests.exceptions.ReadTimeout:
        print(Fore.RED + "⚠️ Server Timeout. Try again later.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"⚠️ Network error: {e}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Error: {e}")

# === Main CLI ===
def main():
    os.system("clear")
    show_banner()
    while True:
        try:
            type_effect(Fore.BLUE + "\n📞 Enter Your 10 Digit Number (or 'exit' to quit):")
            number = input(Fore.LIGHTGREEN_EX + "Target ➤ ")
            if number.lower() == "exit":
                break
            if number.isdigit() and len(number) == 10:
                search_number(number)
                # Add a small random delay to avoid rate limiting (optional)
                time.sleep(random.uniform(1, 3))
            else:
                print(Fore.RED + "❌ Invalid number. Please enter exactly 10 digits.")
        except KeyboardInterrupt:
            print(Fore.RED + "\n⛔ Exiting...")
            break

# === Entry Point ===
if __name__ == "__main__":
    main()