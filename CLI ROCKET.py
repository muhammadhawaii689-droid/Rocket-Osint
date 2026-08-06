#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
┌──────────────────────────────────────────────────────────────┐
│  ROCKET v3.0 - INDIA EDITION                      │
│  dev @rocketxd555  •  zero network  •  zero keys              │
│  Local intelligence for Indian mobile / landline / shortcodes │
└──────────────────────────────────────────────────────────────┘
"""
import sys, time, json, random, hashlib, re, argparse, shutil, textwrap

try:
    import colorama
    colorama.init(convert=True)
except ImportError:
    colorama = None

RESET = "\x1b[0m"; BOLD = "\x1b[1m"; DIM = "\x1b[2m"

def fg(r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m"

def hue2rgb(h):
    c = 255
    x = int(c * (1 - abs((h % 360) / 60 % 2 - 1)))
    h %= 360
    if h < 60:   return (c, x, 0)
    if h < 120:  return (x, c, 0)
    if h < 180:  return (0, c, x)
    if h < 240:  return (0, x, c)
    if h < 300:  return (x, 0, c)
    return (c, 0, x)

# ════════════════════════════ INDIA TELECOM INTELLIGENCE ═══════════════════════════════════════

SERIES_ERA = {  # first digit -> era + original allocation style (legacy lore)
    "9": "LEGACY SERIES (1995-2010) - early GSM/CDMA allocation, spread across Airtel / Vodafone-Idea / BSNL / MTNL",
    "8": "MODERN SERIES (2010s) - heavy Jio allocation post-2016, also Airtel / Vi / BSNL",
    "7": "MODERN SERIES (2010s-2020s) - predominantly Jio, also Airtel / Vi / BSNL",
    "6": "NEW SERIES (2015+) - fresh allocations, Jio / Airtel / Vi / BSNL",
}

PREFIX_LORE = {  # legacy DoT allocation (pre-MNP, approximate) prefix: (operator, circle)
    "9810": ("Airtel", "Delhi"),   "9811": ("Vodafone", "Delhi"),
    "9818": ("Airtel", "Delhi"),   "9868": ("Vodafone", "Delhi"),
    "9873": ("Vodafone", "Delhi"), "9899": ("Vodafone", "Delhi"),
    "9910": ("Airtel", "Delhi"),   "9958": ("Airtel", "Delhi"),
    "9999": ("Airtel", "Delhi"),
    "9820": ("Airtel", "Mumbai"),  "9821": ("Airtel", "Mumbai"),
    "9822": ("Vodafone", "Mumbai"),"9869": ("Vodafone", "Mumbai"),
    "9987": ("Vodafone", "Mumbai"),"9920": ("Airtel", "Mumbai"),
    "9830": ("Airtel", "Kolkata"), "9831": ("Airtel", "Kolkata"),
    "9836": ("Airtel", "Kolkata"), "9903": ("Airtel", "Kolkata"),
    "9840": ("Airtel", "Chennai"), "9841": ("Airtel", "Chennai"),
    "9884": ("Airtel", "Chennai"),
    "9845": ("Airtel", "Bangalore"), "9886": ("Airtel", "Bangalore"),
    "9900": ("Airtel", "Bangalore"),
    "9849": ("Airtel", "Hyderabad"), "9949": ("Airtel", "Hyderabad"),
    "9895": ("Airtel", "Pune"),
}

STD_CODES = {  # well-established landline STD codes
    "011":"Delhi NCR",          "022":"Mumbai",        "033":"Kolkata",
    "044":"Chennai",            "040":"Hyderabad",     "080":"Bengaluru",
    "020":"Pune",               "079":"Ahmedabad",     "0120":"Noida / Ghaziabad",
    "0124":"Gurugram",          "0129":"Faridabad",    "0135":"Dehradun",
    "0141":"Jaipur",            "0161":"Ludhiana",     "0172":"Chandigarh",
    "0177":"Shimla",            "0183":"Amritsar",     "0191":"Jammu",
    "0194":"Srinagar",          "0240":"Aurangabad",   "0241":"Ahmednagar",
    "0253":"Nashik",            "0261":"Surat",        "0265":"Vadodara",
    "0281":"Rajkot",            "0291":"Jodhpur",      "0294":"Udaipur",
    "0413":"Puducherry",        "0422":"Coimbatore",   "0427":"Salem",
    "0431":"Tiruchirappalli",   "0452":"Madurai",      "0471":"Thiruvananthapuram",
    "0481":"Kottayam",          "0484":"Kochi",        "0487":"Thrissur",
    "0495":"Kozhikode",         "0512":"Kanpur",       "0522":"Lucknow",
    "0542":"Varanasi",          "0562":"Agra",         "0612":"Patna",
    "0651":"Ranchi",            "0657":"Jamshedpur",   "0671":"Cuttack",
    "0674":"Bhubaneswar",       "0712":"Nagpur",       "0731":"Indore",
    "0751":"Gwalior",           "0755":"Bhopal",       "0771":"Raipur",
    "0821":"Mysuru",            "0824":"Mangaluru",    "0832":"Panaji (Goa)",
    "0863":"Guntur",            "0866":"Vijayawada",   "0891":"Visakhapatnam",
}

SHORTCODES = {  # emergency / service codes
    "100":"POLICE",          "101":"FIRE",          "102":"AMBULANCE",
    "108":"EMERGENCY (state)", "112":"UNIFIED EMERGENCY (national)",
    "139":"RAILWAY ENQUIRY", "181":"WOMEN HELPLINE","1091":"WOMEN DISTRESS",
    "1098":"CHILDLINE",      "1930":"CYBERCRIME",
}

LEET = ["1337","80085","666","420","69","007","31337","777777"]

# ════════════════════════════ ANIMATION ENGINES ════════════════════════════════════════════════

def _char(color, ch):
    sys.stdout.write(color + ch); sys.stdout.flush()

def type_text(text, mode, cps, seed=None):
    rnd = random.Random(seed)
    base = 1.0 / max(1, cps)
    for i, ch in enumerate(text):
        if mode == "rainbow":
            c = fg(*hue2rgb((i * 18) % 360))
        elif mode == "matrix":
            c = fg(0, rnd.randint(130, 255), rnd.randint(0, 70))
        elif mode == "neon":
            c = fg(*rnd.choice([(0,255,255),(255,0,255),(255,255,0)]))
        elif mode == "cyber":
            c = fg(*rnd.choice([(255,80,200),(0,255,255),(120,255,80),(255,200,0),(160,120,255)]))
        else:
            c = fg(0, 255, 140)
        _char(c, ch)
        time.sleep(base * rnd.uniform(0.6, 1.4))
    sys.stdout.write(RESET + "\n"); sys.stdout.flush()

def banner():
    art = [
        " ██████╗  ██████╗  ███████╗██╗  ██╗███████╗███████╗",
        " ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔════╝",
        " ██████╔╝██║   ██║███████╗█████╔╝ █████╗  ███████╗",
        " ██╔══██╗██║   ██║╚════██║██╔═██╗ ██╔══╝  ╚════██║",
        " ██║  ██║╚██████╔╝███████║██║  ██╗███████╗███████║",
        " ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝",
    ]
    for line in art:
        for i, ch in enumerate(line):
            _char(fg(*hue2rgb((i * 6 + random.randint(-4, 4)) % 360)), ch)
        sys.stdout.write(RESET + "\n"); sys.stdout.flush()
        time.sleep(0.05)
    type_text(f"{DIM}v3.0 INDIA EDITION  •  +91 ONLY  •  dev @rocketxd555{RESET}", "cyber", 60)
    print()

# ════════════════════════════ ANALYSIS ENGINE (+91) ════════════════════════════════════════════

def normalize(raw):
    d = re.sub(r"\D", "", raw or "")
    if d.startswith("91") and len(d) > 10:   # +91 98765 43210 -> 9876543210
        d = d[2:]
    elif d.startswith("0") and len(d) > 10:  # 0 98765 43210
        d = d[1:]
    return d

def match_std(d):
    """longest STD prefix match on a 10-digit national number"""
    for ln in (4, 3, 2):
        if d[:ln] in STD_CODES:
            return ln, STD_CODES[d[:ln]]
    return None, None

def analyze(raw):
    d = normalize(raw)
    if not d:
        return {"error": "empty input"}
    if len(d) <= 5:                                   # shortcode
        if d in SHORTCODES:
            return {"input": raw.strip(), "type": "SERVICE / SHORTCODE",
                    "code": d, "meaning": SHORTCODES[d]}
        return {"error": f"{d} - unrecognized short code"}
    if d.startswith("1800"):                          # toll-free
        return {"input": raw.strip(), "type": "TOLL-FREE",
                "e164": "+91 " + " ".join(d[i:i+4] for i in range(0, len(d), 4)),
                "note": "1800 series - national toll-free (NDNC-style 1-800 services)"}

    if len(d) != 10:
        return {"error": f"invalid length: {len(d)} digits (expect 10 for +91)"}

    # landline check first (STD prefixes can start 6-9 in Bihar/Odisha/Jharkhand)
    ln, city = match_std(d)
    if ln:
        return {
            "input": raw.strip(), "type": "LANDLINE",
            "e164": "+91 " + d, "std": "0" + d[:ln],
            "std_city": city, "subscriber": d[ln:],
            "national": f"0{d[:ln]} {d[ln:]}",
            "flags": [], "pattern_score": 0, "anomaly": anomaly_score(d),
        }

    if d[0] not in "6789":
        return {"error": f"'{d[0]}' series is not a valid Indian mobile prefix (mobile = 6/7/8/9); looks like landline w/o matching STD table"}

    lore = None
    for ln in (4, 3):
        if d[:ln] in PREFIX_LORE:
            lore = (d[:ln], PREFIX_LORE[d[:ln]]); break
    flags, pscore = patterns(d)
    return {
        "input": raw.strip(),
        "type": "MOBILE",
        "e164": "+91 " + d[:5] + " " + d[5:],
        "national": d[:5] + " " + d[5:],
        "dotted": "+91." + ".".join(d[i:i+3] for i in range(0, 10, 3)),
        "series": d[0], "series_era": SERIES_ERA[d[0]],
        "lore": lore, "mnp": "MNP since 2011 - current operator can differ from original allocation",
        "flags": flags, "pattern_score": pscore, "anomaly": anomaly_score(d),
    }

def patterns(d):
    flags, score = [], 0
    if len(set(d)) == 1:            flags.append("ALL-SAME-DIGIT"); score += 30
    if d == d[::-1] and len(d) >= 4:flags.append("PALINDROME"); score += 15
    if all(int(b)-int(a) == 1 for a, b in zip(d, d[1:])):
        flags.append("SEQUENTIAL-ASC"); score += 15
    if all(int(a)-int(b) == 1 for a, b in zip(d, d[1:])):
        flags.append("SEQUENTIAL-DESC"); score += 15
    for s in LEET:
        if s in d: flags.append(f"LEET[{s}]"); score += 8
    if len(set(d)) <= 3:            flags.append("LOW-ENTROPY"); score += 10
    return flags, min(score, 100)

def anomaly_score(d):
    h = int.from_bytes(hashlib.sha256(d.encode()).digest()[:2], "big")
    _, p = patterns(d)
    return min(99, h % 71 + p)

# ════════════════════════════ RENDER (MODIFIED WITH WRAPPING) ══════════════════════════════════

def render(data, mode, cps, json_out=False):
    if json_out:
        print(json.dumps(data, indent=2, ensure_ascii=False)); return
    if "error" in data:
        type_text(f"[!] {data['error']}", "neon", cps); return

    # Calculate wrap width ~75% of terminal columns
    try:
        cols = shutil.get_terminal_size().columns
        max_width = int(cols * 0.75)
        if max_width < 40:
            max_width = 40
    except:
        max_width = 60

    # Helper to print a wrapped line with typing animation
    def emit(label, value, color_mode):
        if value is None or value == "" or value == [] or value == {}:
            return
        # Build the line: label + value
        full = f"{BOLD}{label:<13}{RESET} : {value}"
        # Wrap; subsequent lines indented to align with the value part
        indent = " " * 16  # 13 (label width) + " : " (3 chars) = 16
        wrapped = textwrap.wrap(full, width=max_width, subsequent_indent=indent)
        for line in wrapped:
            type_text(line, color_mode, cps)

    type_text(f"{BOLD} TARGET RECORD {RESET}", mode, cps * 3)

    rows = [
        ("type", "Type", mode), ("e164", "E.164", "rainbow"),
        ("national", "National", "cyber"), ("dotted", "Dotted", "neon"),
        ("std", "STD", mode), ("std_city", "STD City", "rainbow"),
        ("subscriber", "Subscriber", "cyber"), ("code", "Code", mode),
        ("meaning", "Meaning", "neon"), ("series", "Series", mode),
        ("series_era", "Series Era", "cyber"), ("note", "Note", "rainbow"),
    ]
    for key, label, m in rows:
        emit(label, data.get(key), m)

    if data.get("lore"):
        pref, (op, circle) = data["lore"]
        emit("Orig. Alloc", f"{pref}xxxx  ->  {op} / {circle}  (legacy lore)", "cyber")
    if data.get("mnp"):
        emit("MNP Advisory", data['mnp'], "matrix")
    if data.get("flags"):
        flags_str = "  ".join(f"[{f}]" for f in data["flags"])
        emit("Patterns", flags_str, "cyber")
    if "anomaly" in data:
        emit("Anomaly", f"{data['anomaly']}/99 (deterministic heuristic)", "neon")
    print()

def outro(cps):
    type_text("▀ shutdown complete ▀", "matrix", cps * 3)

# ════════════════════════════ CLI ══════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="ROCKET v3.0 - India edition (+91 only)")
    ap.add_argument("number", nargs="?", help="target +91 number / shortcode")
    ap.add_argument("--anim", choices=["rainbow","matrix","neon","cyber","mono"],
                    default="rainbow")
    ap.add_argument("--cps", type=float, default=22)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-banner", action="store_true")
    ap.add_argument("--std", action="store_true", help="dump bundled STD code DB")
    ap.add_argument("--services", action="store_true", help="dump service shortcodes")
    args = ap.parse_args()

    if not args.no_banner and not args.json:
        banner()

    if args.std:
        for code, city in sorted(STD_CODES.items(), key=lambda x: -len(x[0])):
            type_text(f"0{code:<5} {city}", "cyber", args.cps * 2)
        return
    if args.services:
        for code, name in sorted(SHORTCODES.items(), key=lambda x: -len(x[0])):
            type_text(f"{code:<5} {name}", "neon", args.cps * 2)
        return

    if args.number:
        render(analyze(args.number), args.anim, args.cps, args.json)
        if not args.json: outro(args.cps)
        return

    if not args.json:
        type_text("interactive mode - +91 number or shortcode, 'q' to exit", "neon", args.cps * 2)
    while True:
        try:
            n = input(f"{fg(0,255,140)}rocket{fg(160,120,255)}> {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if n.lower() in ("q", "quit", "exit"): break
        if not n: continue
        render(analyze(n), args.anim, args.cps, args.json)
    if not args.json: outro(args.cps)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        type_text("aborted.", "neon", 30)
        sys.exit(130)