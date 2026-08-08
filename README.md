   ROCKET xD - Number Lookup Tool (Termux / Linux CLI)

🚀 DESCRIPTION
--------------
This is a CLI-based phone number lookup tool that fetches
details from the FTOSINT API. It
displays information such as name, address, circle, alternate
number, and more. The output is formatted in a clean, colored
text with a typing animation for a vintage terminal feel.

The tool is designed for Termux but works on any Linux
environment with Python 3.6+.

📦 FEATURES
------------
- ✅ Fast and simple 10-digit number lookup
- ✅ Beautiful colored terminal output (using colorama)
- ✅ Typing/slow‑print animation for results
- ✅ Robust JSON parsing – handles raw API responses with extra text
- ✅ Automatic extraction of multiple result entries
- ✅ Built‑in error handling for timeouts, invalid numbers, etc.
- ✅ Keyboard interrupt (Ctrl+C) friendly
- ✅ Random delay between requests to avoid rate limits

🔧 REQUIREMENTS
----------------
- Python 3.6 or higher
- pip (Python package manager)
- Internet connection (to call the API)

Dependencies (installed via requirements.txt):
- requests
- colorama

📥 INSTALLATION (Termux / Linux)
--------------------------------
1. Open Termux (or a Linux terminal) and run the following commands:

   pkg update && pkg upgrade -y
   pkg install python git -y
   git clone https://github.com/muhammadhawaii689-droid/Rocket-Osint.git
   cd Rocket-Osint
   pip install -r requirements.txt
   python "CLI ROCKET.py"

🚀 USAGE
---------
1. Launch the script (see installation step 2).
2. You will see the banner and a prompt: "Enter Your 10 Digit Number".
3. Type a valid 10-digit Indian mobile number (e.g., 9876543210) and press Enter.
4. The tool will query the API and display the results with a typing animation.
5. After the result, you can enter another number or type 'exit' to quit.

Example:
--------
Target ➤ 9876543210

📊 Search Results for 9876543210

==================================================
 Result #1
==================================================

mobile: 9876543210
name: John Doe
address: 123 Main St, City, State
...
==================================================

⚡ Made by Rocket xD
👉 Join: https://t.me/rocket_xd777

⚠️ TROUBLESHOOTING
-------------------
- "Invalid number" : Ensure you enter exactly 10 digits, no spaces.
- "No results found": The number might not be in the database. Try another.
- "Server Timeout"  : The API server may be slow; try again later.
- "Failed to extract JSON": The response format may have changed. Check the raw output printed in the terminal for debugging.
- "Network error"   : Check your internet connection and ensure the API endpoint is reachable.

If you face persistent issues, join the Telegram channel for support:
https://t.me/rocket_xd777

===============================================================
📄 CREDITS & LICENSE
---------------------
- Script developed by: Rocket xD
- API provided by: FTOSINT
- Banner and design inspired by Termux style.

This tool is for educational and informational purposes only.
Use responsibly and respect privacy laws. The author is not
responsible for any misuse.

Enjoy! 🚀
===============================================================
