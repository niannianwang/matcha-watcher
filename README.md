# Marukyu Koyamaen Matcha Restock Watcher

Watches the 11 "Principal matcha" products on Marukyu Koyamaen and sends a phone notification the moment any of them comes back in stock.

It checks every couple of hours, runs for free on GitHub Actions, and keeps working when your computer is off.

Anyone is welcome to fork this and use it for themselves or directly setup notifications on their device.

## How it works

1. A scheduled GitHub Actions workflow runs `check_stock.py`.
2. The script loads each product page and looks for the phrase the site shows when an item is sold out.
3. It compares the result to `state.json`, which stores what was in or out of stock on the previous run.
4. If a product flips from out of stock to in stock, it sends a push notification through [ntfy](https://ntfy.sh). You only get notified on a change, never on every run.
5. The workflow saves the updated `state.json` back to the repo for the next run.

## Setup notification for yourself! (about 5 minutes)

- Install **ntfy** on your phone: [iOS](https://apps.apple.com/us/app/ntfy/id1625396347) or [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
- Open the app, tap **+**, and subscribe to a topic.
- Type in koyamaen-matcha
- Press Subscribe
- Finally, turn on allow notifcations for ntfy app!

## When it fires

You get a notification titled something like "🍵 Wako is back in stock!". If several products restock at once, you get a single notification listing all of them.

These items sell out fast, so before a restock happens:

- Register and log in at marukyu-koyamaen.co.jp. The site requires an account to buy ([register here](https://www.marukyu-koyamaen.co.jp/english/shop/account)).
- Save your payment and shipping info in your account so checkout takes seconds.

## Customizing this script

- **Products:** edit the `PRODUCTS` list in `check_stock.py`. Each entry is a name and a product page URL.
- **Sold out phrase:** if the site ever changes its wording, update `OUT_OF_STOCK_MARKER`. If that phrase stops matching, every product will look in stock, so check this first when you get a burst of false alerts.
- **Frequency:** change the `cron` line in the workflow file.

## Notes and limitations

- GitHub's free scheduled jobs are not precise. Expect a delay depending on GitHub's load.
- The script treats a product page as in stock when the sold out phrase is missing. Some products come in multiple sizes, so it fires when any size becomes buyable.
- Keep the 1 second pause between requests so the shop's server is not hammered.
