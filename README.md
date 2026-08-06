
   ROCKET v3.0 - INDIA EDITION (Termux Guide)
   dev: @rocketxd555  |  Forked & Modified

🔹 YEH KYA HAI?
Ye tool hai Indian mobile numbers (+91), landline (STD codes), aur emergency shortcodes ki intelligence lene ke liye. Isme kisi API key ya internet ki zaroorat nahi hai – sab kuch local run hota hai.

🔹 NAYA FEATURE (MODIFIED VERSION):
Abhi is modified version mein result screen ke 70-80% width mein aata hai (poora screen nahi bharta) aur typing animation ke saath aata hai – leaks chain ke numbers ke liye perfect hai.

================================================
📲 TERMUX MEIN INSTALL KAISE KAREIN?
================================================

   pkg update && pkg upgrade -y
   
   pkg install python git -y
   
   git clone https://github.com/muhammadhawaii689-droid/Rocket-Osint.git
   
   cd Rocket-Osint
   
   pip install -r requirements.txt
   
   (Agar error aaye toh alag se install karo: pip install colorama)
   
   python "CLI ROCKET.py"

================================================
🎮 USE KAISE KAREIN? (COMMANDS)
================================================

🔸 INTERACTIVE MODE (Number daalte raho):
   python "CLI ROCKET.py"

🔸 EK NUMBER KE LIYE (Direct):
   python "CLI ROCKET.py" 9876543210

🔸 ANIMATION CHANGE KARO (rainbow, matrix, neon, cyber):
   python "CLI ROCKET.py" 9876543210 --anim neon

🔸 TYPING SPEED SLOW/FAST KARO (default 22 cps):
   python "CLI ROCKET.py" 9876543210 --cps 15

🔸 BANNER HATAAO (chhota screen ke liye):
   python "CLI ROCKET.py" 9876543210 --no-banner

🔸 JSON OUTPUT (Raw data ke liye):
   python "CLI ROCKET.py" 9876543210 --json

🔸 SARI STD CODES DEKHO:
   python "CLI ROCKET.py" --std

🔸 EMERGENCY SHORTCODES DEKHO:
   python "CLI ROCKET.py" --services

================================================
📝 EXAMPLE (BEST COMBO):
================================================
python "CLI ROCKET.py" 9876543210 --anim rainbow --cps 20 --no-banner

Isse output wrapped (screen ke 75% width mein) aur typing animation ke saath aayega, banner nahi aayega.

================================================
⚠️ DISCLAIMER (ZAROORI):
================================================
Ye tool sirf EDUCATIONAL aur ETHICAL purposes ke liye hai. Kisi ki privacy breach karna ya illegal surveillance karna strictily prohibited hai. Is tool ka use karte waqt apne local laws ka dhyan rakhein.

================================================
💬 KOI ISSUE?
================================================
Agar koi error aata hai (jaise module not found), toh bina dare comment karo. Main help kar dunga!

Happy Hacking! 🐧🔥
