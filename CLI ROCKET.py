#!/usr/bin/env python3

"""
ROCKET — animated number-info CLI for Termux
API : https://num-info-demo.hcjffjggjf.workers.dev/?number=<NUMBER>
"""

import sys, os, re, json, time, signal, argparse, threading
import urllib.request, urllib.error, urllib.parse

VERSION = "1.0.0"
API_URL = "https://num-info-demo.hcjffjggjf.workers.dev/?number={}"

# ─────────────────────────── ANSI ───────────────────────────
R, B = "\x1b[0m", "\x1b[1m"
C_RED, C_GREEN, C_YELLOW = "31", "32", "33"
C_BLUE, C_MAGENTA, C_CYAN, C_WHITE = "34", "35", "36", "37"
RAINBOW = [C_RED, C_YELLOW, C_GREEN, C_CYAN, C_BLUE, C_MAGENTA]

def fg(code, text, bold=False):
    return f"\x1b[{code}m" + (B if bold else "") + text + R

def rainbow(text, shift=0, bold=False):
    out, i = [], 0
    for ch in text:
        if ch == " ":
            out.append(" ")
        else:
            out.append(fg(RAINBOW[(i + shift) % len(RAINBOW)], ch, bold))
            i += 1
    return "".join(out)

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
def vlen(s):
    return len(ANSI_RE.sub("", s))

def clear():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()

# ─────────────────────────── ART ───────────────────────────
BANNER = [
    "██████╗  ██████╗  ██████╗██╗  ██╗███████╗████████╗",
    "██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝",
    "██████╔╝██║   ██║██║     █████╔╝ █████╗     ██║   ",
    "██╔══██╗██║   ██║██║     ██╔═██╗ ██╔══╝     ██║   ",
    "██║  ██║╚██████╔╝╚██████╗██║  ██╗███████╗   ██║   ",
    "╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ",
]

ROCKET_BODY = [
    "      ▲",
    "     ▲▲▲",
    "    ▲▲▲▲▲",
    "   ▲▲▲▲▲▲▲",
    "   █████████",
    "   █  ███  █",
    "   █  ███  █",
    "   █       █",
    "   █████████",
]

FLAMES = [
    ["      ███", "      ███", "     █████"],
    ["     █████", "      ███", "    ███████"],
    ["      ███", "     █████", "     █████"],
]

def launch_rocket(steps=16, delay=0.03):
    stars = fg(C_WHITE, "  ✦   .  ✧  .  ✦   .  ✧  .  ✦\n")
    for step in range(steps):
        clear()
        sys.stdout.write(stars)
        for _ in range(steps - step - 1):
            sys.stdout.write("\n")
        flame = FLAMES[step % len(FLAMES)]
        body = ROCKET_BODY + flame
        for i, line in enumerate(body):
            if i < 4:            col = C_WHITE
            elif i < 8:          col = C_CYAN
            elif i == 8:         col = C_BLUE
            else:                col = C_YELLOW if i % 2 == 0 else C_RED
            sys.stdout.write(fg(col, B + line) + "\n")
        sys.stdout.flush()
        time.sleep(delay)
    clear()
    for _ in range(3):
        sys.stdout.write(rainbow("   ✦  ✧  ★  ✦  ✧  ★  ✦  ✧  ★\n", shift=int(time.time() * 20)))
        time.sleep(0.15)
    time.sleep(0.2)

def intro():
    for shift in range(24):          # animated rainbow banner
        clear()
        sys.stdout.write("\n\n")
        for line in BANNER:
            sys.stdout.write(rainbow(line, shift, bold=True) + "\n")
        sys.stdout.write("\n" + fg(C_CYAN, B + "   N U M B E R   I N T E L   S Y S T E M") + "\n")
        sys.stdout.write(fg(C_YELLOW, "        TERMUX EDITION  •  v" + VERSION) + "\n")
        sys.stdout.flush()
        time.sleep(0.05)
    clear()
    sys.stdout.write("\n\n")
    for line in BANNER:
        sys.stdout.write(rainbow(line, 0, True) + "\n")
    sys.stdout.write("\n" + fg(C_CYAN, B + "   N U M B E R   I N T E L   S Y S T E M") + "\n")
    sys.stdout.write(fg(C_YELLOW, "        TERMUX EDITION  •  v" + VERSION) + "\n")
    sys.stdout.flush()
    time.sleep(0.6)
    launch_rocket()

# ─────────────────────────── CORE ───────────────────────────
def fetch(number):
    url = API_URL.format(urllib.parse.quote(number))
    req = urllib.request.Request(url, headers={"User-Agent": f"ROCKET/{VERSION} (Termux CLI)"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))

def fetch_with_spinner(number, anim):
    holder = {}
    def worker():
        try:
            holder["data"] = fetch(number)
        except Exception as exc:
            holder["error"] = exc
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    if anim:
        i = 0
        while thread.is_alive():
            dots = "." * ((i // 3) % 4)
            sys.stdout.write("\r" + fg(C_CYAN, frames[i % len(frames)]) +
                             fg(C_YELLOW, B + "  QUERYING SPACE STATION" + dots) + " " * 8)
            sys.stdout.flush()
            i += 1
            time.sleep(0.07)
        sys.stdout.write("\r" + " " * 60 + "\r")
    else:
        print(fg(C_YELLOW, "Fetching number info..."))
    thread.join()
    if "error" in holder:
        raise holder["error"]
    return holder["data"]

# ─────────────────────────── UI ───────────────────────────
def box(title, body, width=None):
    if width is None:
        width = max([vlen(x) for x in body] + [vlen(title) + 2] + [46])
    out = [fg(C_CYAN, "╔" + "═" * (width + 2) + "╗")]
    if title:
        out.append(fg(C_CYAN, "║ ") + fg(C_YELLOW, B + title) + " " * (width - vlen(title)) + fg(C_CYAN, " ║"))
        out.append(fg(C_CYAN, "╠" + "═" * (width + 2) + "╣"))
    for ln in body:
        out.append(fg(C_CYAN, "║ ") + ln + " " * (width - vlen(ln)) + fg(C_CYAN, " ║"))
    out.append(fg(C_CYAN, "╚" + "═" * (width + 2) + "╝"))
    return "\n".join(out)

def usage_bar(remaining, total=100, width=12):
    pct = max(0.0, min(1.0, remaining / total))
    filled = int(round(pct * width))
    return fg(C_GREEN, "█" * filled) + fg(C_RED, "░" * (width - filled))

def render_result(result):
    lines = []
    if isinstance(result, dict):
        if "detail" in result:
            detail = str(result["detail"])
            lines.append(fg(C_RED, B + "⚠  " + detail))
            low = detail.lower()
            if "forbidden" in low or "unauthorized" in low:
                lines.append(fg(C_YELLOW, "   The demo key may not have NUM access."))
                lines.append(fg(C_YELLOW, "   Use a key with NUM permission, or check the API docs."))
            return lines
        for k, v in result.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v, ensure_ascii=False)
            lines.append(fg(C_GREEN, B + "▸ " + k) + fg(C_WHITE, "  " + str(v)))
    else:
        lines.append(fg(C_WHITE, str(result)))
    return lines

def show_result(number, data):
    status = data.get("status")
    remaining = data.get("remaining_requests")
    developer = data.get("developer", "unknown")
    result = data.get("result")
    status_txt = fg(C_GREEN, B + "● ONLINE") if status else fg(C_RED, B + "● OFFLINE")

    info = [
        fg(C_GREEN, B + "▸ NUMBER")   + fg(C_WHITE, "    " + number),
        fg(C_GREEN, B + "▸ STATUS")   + fg(C_WHITE, "    " + status_txt),
    ]
    if remaining is not None:
        info.append(fg(C_GREEN, B + "▸ REQUESTS") + " " + usage_bar(remaining) + fg(C_WHITE, f"  {remaining} left"))
    if developer:
        info.append(fg(C_GREEN, B + "▸ DEVELOPER") + fg(C_WHITE, " " + developer))

    print()
    print(box("  🚀  ROCKET  —  NUMBER INTEL  ", info))
    print()
    print(box("  ▸  DATA  ", render_result(result) if result is not None else [fg(C_RED, "no data returned")]))
    print()

# ─────────────────────────── HELPERS ───────────────────────────
def clean_number(raw):
    n = str(raw).strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace(".", "")
    if n.startswith("+"):
        n = n[1:]
    if not n.isdigit():
        raise ValueError("Number must contain only digits (plus sign allowed at the start).")
    if not 7 <= len(n) <= 15:
        raise ValueError("Number length looks off — expected 7 to 15 digits.")
    return n

def ask_number():
    sys.stdout.write("\n" + fg(C_YELLOW, B + "  ☎  ENTER PHONE NUMBER") + fg(C_CYAN, "  ➜  "))
    sys.stdout.flush()
    return input().strip()

def _sigint(*_):
    sys.stdout.write("\r" + " " * 60 + "\r")
    print(fg(C_YELLOW, "  👋 Aborted. See you next launch!"))
    sys.exit(130)

# ─────────────────────────── MAIN ───────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="rocket",
        description="ROCKET — animated number-info CLI for Termux",
        epilog="Example: python3 rocket.py 6395954711",
    )
    parser.add_argument("number", nargs="?", help="phone number to look up")
    parser.add_argument("-n", "--number", dest="alt_number", help="same as the positional number")
    parser.add_argument("--json", action="store_true", help="print raw JSON and exit")
    parser.add_argument("--once", action="store_true", help="single lookup then exit")
    parser.add_argument("--no-anim", action="store_true", help="disable animations")
    parser.add_argument("--version", action="version", version=f"ROCKET {VERSION}")
    args = parser.parse_args()

    anim = (not args.no_anim) and sys.stdout.isatty()
    number = args.number or args.alt_number
    if number is not None:
        try:
            number = clean_number(number)
        except ValueError as e:
            print(fg(C_RED, B + "✗ " + str(e)))
            sys.exit(1)

    if anim:
        intro()

    if args.json:
        try:
            number = number or clean_number(ask_number())
            print(json.dumps(fetch_with_spinner(number, anim), indent=2, ensure_ascii=False))
        except Exception as e:
            print(fg(C_RED, B + "✗ LOOKUP FAILED — " + str(e)))
            sys.exit(1)
        sys.exit(0)

    while True:
        try:
            if number is None:
                number = ask_number()
            number = clean_number(number)
            data = fetch_with_spinner(number, anim)
            show_result(number, data)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError,
                json.JSONDecodeError, ValueError) as e:
            print(fg(C_RED, B + "✗ LOOKUP FAILED — " + str(e)))
            number = None
        if args.once:
            break
        sys.stdout.write("\n" + fg(C_CYAN, "  Enter a new number to query again, or ") +
                         fg(C_YELLOW, B + "q") + fg(C_CYAN, " to quit  ➜  "))
        sys.stdout.flush()
        choice = input().strip()
        if choice.lower() in ("q", "quit", "exit", ""):
            break
        number = choice

    print(fg(C_CYAN, "\n  🚀 ROCKET v" + VERSION + " — orbit complete. Launch again anytime!"))

if __name__ == "__main__":
    signal.signal(signal.SIGINT, _sigint)
    main()