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

```bash
pkg update && pkg install python -y
pip install -r requirements.txt
chmod +x rocket.py
python rocket.py
