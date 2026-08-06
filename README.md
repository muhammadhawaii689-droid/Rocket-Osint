# 🚀 ROCKET — Number-Info CLI for Termux

An animated, space-themed command-line tool that queries the **numleak API**
and displays phone-number intelligence (leak records + call-tracer data)
directly in your terminal.

---

## ✨ Features

- 🎆 Animated **rainbow banner** + **rocket launch** intro
- ⏳ Live **braille spinner** while querying the API
- 📦 **LEAK CHAIN** panel — title, description, and full record entries
  (FullName, FatherName, DocumentNumber, addresses, phones, region)
- 📞 **CALL TRACER** panel — SIM, IMEI, MAC, IP, owner address, tower
  locations, helpline, numerology analysis, and more
- 📊 **UNLIMITED** request bar + developer credit `@rocketxd555`
- 🔄 Interactive **multi-lookup loop** (query → query again → quit)
- 🛡️ Graceful handling of API errors and missing data

---

## 📦 Requirements

- **Python 3.6+**
- **Termux** (Android) — also runs on Linux/macOS
- No external Python packages (stdlib only)

---

## 🛠 Installation (Termux)

```bash
pkg update && pkg install python -y
cd ~/Rocket-Osint
chmod +x rocket.py
python rocket.py
