# 🚀 ROCKET — Number Info CLI for Termux

An animated, space-themed command-line tool that queries the **Number Info API**
and displays phone number intelligence in your terminal.

## ✨ Features

- 🎆 Animated **rainbow banner** + **rocket launch** intro
- ⏳ Live **braille spinner** while querying the API
- 📊 Styled panels with a **request-quota usage bar**
- 🔄 Interactive **multi-lookup loop** (query → query again → quit)
- 🛡️ Handles API errors gracefully (e.g. `Key unauthorized`)

## 📦 Requirements

- **Python 3.6+**
- **Termux** (Android) — works on Linux/macOS too
- No external Python packages (stdlib only)

## 🛠 Installation (Termux)

pkg update && pkg upgrade -y

pkg install git python -y

git clone 
https://github.com/muhammadhawaii689-droid/Rocket-Osint.git

cd Rocket-Osint

pip install -r requirements.txt

chmod +x "CLI ROCKET.py"

./"CLI ROCKET.py"
