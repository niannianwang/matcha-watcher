#!/usr/bin/env python3
"""
Marukyu Koyamaen 'Principal matcha' restock watcher.

Checks each product page for the phrase that appears only when a product
is sold out. When a product flips from "out of stock" -> "in stock", it
sends a push notification via ntfy.sh (free, no account needed) so you
can jump on it before it sells out again.

State (what was in/out of stock last run) is persisted to state.json so
we only notify on a *change*, not on every single run.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

# --- Configuration -----------------------------------------------------

# ntfy.sh topic - set this via the NTFY_TOPIC environment variable
# (GitHub Actions secret). Pick a hard-to-guess topic name since anyone
# who knows it can read/post to it. e.g. "matcha-alerts-8f2k1x"
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "")

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

OUT_OF_STOCK_MARKER = "currently out of stock and unavailable"

PRODUCTS = [
    ("Kiwami Choan", "https://www.marukyu-koyamaen.co.jp/english/shop/products/1g36020c1"),
    ("Unkaku",        "https://www.marukyu-koyamaen.co.jp/english/shop/products/1141020c1"),
    ("Wako",          "https://www.marukyu-koyamaen.co.jp/english/shop/products/1161020c1"),
    ("Tenju",         "https://www.marukyu-koyamaen.co.jp/english/shop/products/1111020c1"),
    ("Choan",         "https://www.marukyu-koyamaen.co.jp/english/shop/products/1121020c1"),
    ("Eiju",          "https://www.marukyu-koyamaen.co.jp/english/shop/products/1131020c1"),
    ("Kinrin",        "https://www.marukyu-koyamaen.co.jp/english/shop/products/1151020c1"),
    ("Yugen",         "https://www.marukyu-koyamaen.co.jp/english/shop/products/1171020c1"),
    ("Chigi no Shiro","https://www.marukyu-koyamaen.co.jp/english/shop/products/1181040c1"),
    ("Isuzu",         "https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1"),
    ("Aoarashi",      "https://www.marukyu-koyamaen.co.jp/english/shop/products/11a1040c1"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def is_in_stock(html: str) -> bool:
    """Product page has NO 'out of stock' marker => at least one variant is buyable."""
    return OUT_OF_STOCK_MARKER not in html


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state: dict) -> None:
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def notify(title: str, message: str, url: str) -> None:
    if not NTFY_TOPIC:
        print(f"[NOTIFY - no NTFY_TOPIC set] {title}: {message}")
        return
    # Use ntfy's JSON publish API (not custom HTTP headers) so emoji/UTF-8
    # in the title/message don't break header encoding (headers are
    # latin-1 only; JSON body is UTF-8 safe).
    payload = json.dumps({
        "topic": NTFY_TOPIC,
        "title": title,
        "message": message,
        "priority": "max",
        "tags": ["tea", "rotating_light"],
        "click": url,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://ntfy.sh/",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=15)
        print(f"Notification sent: {title}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"Failed to send notification: HTTP {e.code} - {body}")
    except urllib.error.URLError as e:
        print(f"Failed to send notification: {e}")


def main() -> None:
    state = load_state()
    new_state = {}
    changes = []

    for name, url in PRODUCTS:
        try:
            html = fetch(url)
        except Exception as e:
            print(f"Error fetching {name} ({url}): {e}")
            # Keep previous known state if fetch fails, don't wipe it out
            new_state[name] = state.get(name, {}).get("in_stock", False)
            continue

        in_stock = is_in_stock(html)
        was_in_stock = state.get(name, {}).get("in_stock", False)
        new_state[name] = {"in_stock": in_stock, "checked_at": int(time.time())}

        status = "IN STOCK" if in_stock else "out of stock"
        print(f"{name}: {status}")

        if in_stock and not was_in_stock:
            changes.append((name, url))

        time.sleep(1)  # be polite to their server

    save_state(new_state)

    if changes:
        try:
            if len(changes) == 1:
                name, url = changes[0]
                notify(
                    f"🍵 {name} is back in stock!",
                    f"{name} just restocked on Marukyu Koyamaen. Go go go!",
                    url,
                )
            else:
                names = ", ".join(n for n, _ in changes)
                notify(
                    f"🍵 {len(changes)} matcha products restocked!",
                    f"Back in stock: {names}",
                    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/principal",
                )
        except Exception as e:
            # Never let a notification failure crash the run - state is
            # already saved above, and we'd rather log the error than
            # silently get stuck re-trying (and failing) every 5 minutes.
            print(f"Notification error (state was still saved): {e}")
    else:
        print("No changes since last check.")


if __name__ == "__main__":
    main()
