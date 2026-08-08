import requests
import json
import os
import time
import random
from colorama import init, Fore, Style

init(autoreset=True)

# === CONFIGURATION ===
API_BASE = "https://ftosint.world/api/number?key=demo-4-rocket&num="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) Gecko/117.0 Firefox/117.0",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://rocket-xd.vercel.app/",
    "Connection": "keep-alive"
}

# === Typing Animation ===
def type_effect(text, delay=0.002):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# === Swipe-style Text Animation ===
def swipe_effect(text, delay=0.01):
    for line in text.splitlines():
        for char in line:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

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

# === Pretty Print a Single Record ===
def pretty_print_record(record, index):
    """Display a single result with a clear header and formatted fields."""
    print(Fore.LIGHTRED_EX + f"\n{'='*50}")
    print(Fore.LIGHTRED_EX + f" Result #{index} ")
    print(Fore.LIGHTRED_EX + f"{'='*50}\n")

    if isinstance(record, dict):
        for key, value in record.items():
            if isinstance(value, (dict, list)):
                # Pretty‑print nested structures with indentation
                value_str = json.dumps(value, indent=2, ensure_ascii=False)
                # Indent each line further for visual clarity
                value_str = "\n".join("    " + line for line in value_str.splitlines())
                print(Fore.CYAN + f"{key}:")
                print(Fore.WHITE + value_str)
            else:
                print(Fore.YELLOW + f"{key}: " + Fore.WHITE + f"{value}")
    else:
        # Fallback for non‑dict records (should not happen, but just in case)
        print(Fore.WHITE + str(record))

    print(Fore.LIGHTRED_EX + f"{'='*50}\n")

# === Normalize API response into list of dicts ===
def normalize_response(data):
    """
    Accepts the parsed JSON data and returns a list of record-dicts to display.
    Tries several common shapes so it is robust to small API changes.
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

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    data = json.loads(raw_text[start:end+1])
                except Exception:
                    print(Fore.RED + "⚠️ Unable to parse JSON response from server.")
                    return
            else:
                print(Fore.RED + "⚠️ Invalid response format from server.")
                return

        records = normalize_response(data)

        if not records:
            print(Fore.YELLOW + "⚠️ No results found.")
            return

        swipe_effect(Fore.CYAN + f"\n📊 Search Results for {number}\n")

        for idx, user in enumerate(records, 1):
            pretty_print_record(user, idx)

        print(Fore.RED + "\n⚡ Made by Rocket xD")
        print(Fore.BLUE + "👉 Join: https://t.me/rocket_xd777\n")

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
            else:
                print(Fore.RED + "❌ Invalid number. Please enter exactly 10 digits.")
        except KeyboardInterrupt:
            print(Fore.RED + "\n⛔ Exiting...")
            break

# === Entry Point ===
if __name__ == "__main__":
    main()