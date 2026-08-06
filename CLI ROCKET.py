#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROCKET — animated Number-Info CLI for Termux
API : https://ftosint.world/api/number?key=demo-4-rocket&num={}
Dev : @rocketxd555  |  Requests: UNLIMITED
"""

import sys, re, json, time, signal, argparse, threading
import urllib.request, urllib.error, urllib.parse
import ssl  # for SSL fallback
import os   # to detect terminal width

VERSION = "2.0.3"
API_URL = "https://ftosint.world/api/number?key=demo-4-rocket&num={}"

# ─────────────────────────── ANSI ───────────────────────────
R, B = "\x1b[0m", "\x1b[1m"
RAINBOW = ["31", "33", "32", "36", "34", "35"]

def fg(code, text, bold=False):
    return f"\x1b[{code}m" + (B if bold else "") + text + R

def rainbow(text, shift=0, bold=False):
    out, i = [], 0
    for ch in text:
        out.append(" " if ch == " " else fg(RAINBOW[(i + shift) % 6], ch, bold))
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
    "      ▲", "     ▲▲▲", "    ▲▲▲▲▲", "   ▲▲▲▲▲▲▲",
    "   █████████", "   █  ███  █", "   █  ███  █", "   █       █",
    "   █████████",
]
FLAMES = [
    ["      ███", "      ███", "     █████"],
    ["     █████", "      ███", "    ███████"],
    ["      ███", "     █████", "     █████"],
]

def launch_rocket(steps=16, delay=0.03):
    for step in range(steps):
        clear()
        sys.stdout.write(fg("37", "  ✦   .  ✧  .  ✦   .  ✧  .  ✦\n"))
        for _ in range(steps - step - 1):
            sys.stdout.write("\n")
        flame = FLAMES[step % 3]
        body = ROCKET_BODY + flame
        for i, line in enumerate(body):
            col = "37" if i < 4 else "36" if i < 8 else "34" if i == 8 else ("33" if i % 2 == 0 else "31")
            sys.stdout.write(fg(col, B + line) + "\n")
        sys.stdout.flush()
        time.sleep(delay)
    clear()
    for _ in range(3):
        sys.stdout.write(rainbow("   ✦  ✧  ★  ✦  ✧  ★  ✦  ✧  ★\n", shift=int(time.time() * 20)))
        time.sleep(0.15)
    time.sleep(0.2)

def intro():
    for shift in range(24):
        clear()
        sys.stdout.write("\n\n")
        for line in BANNER:
            sys.stdout.write(rainbow(line, shift, True) + "\n")
        sys.stdout.write("\n" + fg("36", B + "   N U M B E R   I N T E L   S Y S T E M") + "\n")
        sys.stdout.write(fg("33", "        TERMUX EDITION  •  v" + VERSION) + "\n")
        sys.stdout.flush()
        time.sleep(0.05)
    clear()
    sys.stdout.write("\n\n")
    for line in BANNER:
        sys.stdout.write(rainbow(line, 0, True) + "\n")
    sys.stdout.write("\n" + fg("36", B + "   N U M B E R   I N T E L   S Y S T E M") + "\n")
    sys.stdout.write(fg("33", "        TERMUX EDITION  •  v" + VERSION) + "\n")
    sys.stdout.flush()
    time.sleep(0.6)
    launch_rocket()

# ─────────────────────────── CORE ───────────────────────────
def fetch(number):
    url = API_URL.format(urllib.parse.quote(number))
    req = urllib.request.Request(url, headers={"User-Agent": f"ROCKET/{VERSION} (Termux CLI)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.URLError as e:
        if "SSL" in str(e):
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(req, timeout=30, context=context) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        raise

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
            sys.stdout.write("\r" + fg("36", frames[i % 10]) +
                             fg("33", B + "  QUERYING LEAK DATABASE" + dots) + " " * 8)
            sys.stdout.flush()
            i += 1
            time.sleep(0.07)
        sys.stdout.write("\r" + " " * 60 + "\r")
    else:
        print(fg("33", "Fetching number info..."))
    thread.join()
    if "error" in holder:
        raise holder["error"]
    return holder["data"]

# ─────────────────────────── UI ───────────────────────────
def get_term_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def box(title, body, width=None):
    if width is None:
        width = max([vlen(x) for x in body] + [vlen(title) + 2] + [46])
    # Ensure width fits terminal
    term_width = get_term_width()
    if width > term_width - 4:
        width = term_width - 4
    out = [fg("36", "╔" + "═" * (width + 2) + "╗")]
    if title:
        out.append(fg("36", "║ ") + fg("33", B + title) + " " * (width - vlen(title)) + fg("36", " ║"))
        out.append(fg("36", "╠" + "═" * (width + 2) + "╣"))
    for ln in body:
        # Truncate if too long
        if vlen(ln) > width:
            ln = ln[:width-3] + "..."
        out.append(fg("36", "║ ") + ln + " " * (width - vlen(ln)) + fg("36", " ║"))
    out.append(fg("36", "╚" + "═" * (width + 2) + "╝"))
    return "\n".join(out)

def kv(k, v):
    return fg("32", B + "▸ " + k) + fg("37", "  " + str(v))

def render_chain(chain):
    lines = []
    if not isinstance(chain, dict):
        lines.append(fg("37", str(chain)))
        return lines
    if chain.get("title"):
        lines.append(fg("35", B + "◉ " + str(chain["title"])))
    if chain.get("description"):
        desc = str(chain["description"])
        while len(desc) > 90:
            lines.append(fg("37", "   " + desc[:90]))
            desc = desc[90:]
        if desc:
            lines.append(fg("37", "   " + desc))
    records = chain.get("records")
    if isinstance(records, list) and records:
        for idx, rec in enumerate(records, 1):
            if not isinstance(rec, dict):
                continue
            lines.append(fg("36", B + f"  ─── RECORD {idx} ───"))
            for k, v in rec.items():
                if isinstance(v, (dict, list)):
                    v = json.dumps(v, ensure_ascii=False)
                lines.append(fg("33", B + "     • " + k) + fg("37", "  " + str(v)))
    return lines

def render_calltracer(ct):
    lines = []
    if not isinstance(ct, dict):
        lines.append(fg("37", str(ct)))
        return lines
    for k, v in ct.items():
        if isinstance(v, (dict, list)):
            v = json.dumps(v, ensure_ascii=False)
        lines.append(kv(k, v))
    return lines

# ─── Typewriter effect ───
def typewriter_print(lines, delay=0.035, anim=True, prefix=None):
    """Print each line with a typing effect."""
    if not anim:
        if prefix:
            print(prefix)
        for line in lines:
            print(line)
        return
    if prefix:
        sys.stdout.write(prefix + "\n")
        sys.stdout.flush()
        time.sleep(0.3)
    for line in lines:
        for ch in line:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(0.02)

def show_result(number, data, anim=True, compact=False):
    success = data.get("success")
    resp_time = data.get("response_time_ms")
    chain = data.get("chain")
    calltracer = data.get("calltracer")

    status_txt = fg("32", B + "● HIT FOUND") if success else fg("31", B + "● NO HIT")

    # Build info lines (always the same)
    info_lines = [
        kv("NUMBER", number),
        kv("STATUS", status_txt),
        kv("REQUESTS", fg("32", B + "█" * 12) + fg("37", "  UNLIMITED")),
        kv("TIME LIMIT", "1 Day"),
        kv("DEVELOPER", "@rocketxd555"),
    ]
    if resp_time is not None:
        info_lines.append(kv("RESPONSE TIME", str(resp_time) + " ms"))

    # Build the entire output as a list of lines (without borders if compact)
    output_lines = []
    if compact:
        # No boxes, just plain colored lines
        output_lines.append("")  # blank line
        output_lines.extend(info_lines)
        output_lines.append("")
        if chain:
            output_lines.append(fg("35", B + "◉ LEAK CHAIN"))
            output_lines.extend(render_chain(chain))
            output_lines.append("")
        if calltracer:
            output_lines.append(fg("35", B + "📞 CALL TRACER"))
            output_lines.extend(render_calltracer(calltracer))
            output_lines.append("")
        if not chain and not calltracer:
            output_lines.append(fg("31", "No data returned for this number."))
            output_lines.append("")
    else:
        # Full boxed UI
        output_lines.append("")
        output_lines.append(box("  🚀  ROCKET  —  NUMBER INTEL  ", info_lines))
        output_lines.append("")
        if chain:
            output_lines.append(box("  ◉  LEAK CHAIN  ", render_chain(chain)))
            output_lines.append("")
        if calltracer:
            output_lines.append(box("  📞  CALL TRACER  ", render_calltracer(calltracer)))
            output_lines.append("")
        if not chain and not calltracer:
            output_lines.append(box("  ▸  DATA  ", [fg("31", "No data returned for this number.")]))
            output_lines.append("")

    # Print with typing animation
    typing_msg = fg("33", B + "  Typing result") + fg("36", " ...")
    typewriter_print(output_lines, anim=anim, prefix=typing_msg)

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
    sys.stdout.write("\n" + fg("33", B + "  ☎  ENTER PHONE NUMBER") + fg("36", "  ➜  "))
    sys.stdout.flush()
    return input().strip()

def _sigint(*_):
    sys.stdout.write("\r" + " " * 60 + "\r")
    print(fg("33", "  👋 Aborted. See you next launch!"))
    sys.exit(130)

# ─────────────────────────── MAIN ───────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="rocket",
        description="ROCKET — animated number-intel CLI for Termux",
        epilog="Example: python3 rocket.py 7505186756",
    )
    parser.add_argument("number", nargs="?", help="phone number to look up")
    parser.add_argument("-n", "--number", dest="alt_number", help="same as the positional number")
    parser.add_argument("--json", action="store_true", help="print raw JSON and exit")
    parser.add_argument("--once", action="store_true", help="single lookup then exit")
    parser.add_argument("--no-anim", action="store_true", help="disable animations (no rocket, no typing)")
    parser.add_argument("--compact", action="store_true", help="use compact output (no borders)")
    parser.add_argument("--version", action="version", version=f"ROCKET {VERSION}")
    args = parser.parse_args()

    anim = (not args.no_anim) and sys.stdout.isatty()
    compact = args.compact or (get_term_width() < 80)  # auto-compact on small screens

    number = args.number or args.alt_number
    if number is not None:
        try:
            number = clean_number(number)
        except ValueError as e:
            print(fg("31", B + "✗ " + str(e)))
            sys.exit(1)

    if anim:
        intro()

    if args.json:
        try:
            number = number or clean_number(ask_number())
            print(json.dumps(fetch_with_spinner(number, anim), indent=2, ensure_ascii=False))
        except Exception as e:
            print(fg("31", B + "✗ LOOKUP FAILED — " + str(e)))
            sys.exit(1)
        sys.exit(0)

    while True:
        try:
            if number is None:
                number = ask_number()
            number = clean_number(number)
            data = fetch_with_spinner(number, anim)
            show_result(number, data, anim=anim, compact=compact)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError,
                json.JSONDecodeError, ValueError) as e:
            print(fg("31", B + "✗ LOOKUP FAILED — " + str(e)))
            number = None
        if args.once:
            break
        sys.stdout.write("\n" + fg("36", "  Enter a new number to query again, or ") +
                         fg("33", B + "q") + fg("36", " to quit  ➜  "))
        sys.stdout.flush()
        choice = input().strip()
        if choice.lower() in ("q", "quit", "exit", ""):
            break
        number = choice

    print(fg("36", "\n  🚀 ROCKET v" + VERSION + " — orbit complete. Launch again anytime!"))

if __name__ == "__main__":
    signal.signal(signal.SIGINT, _sigint)
    main()