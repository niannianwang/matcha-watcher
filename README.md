# Marukyu Koyamaen Matcha Restock Watcher

Watches the 11 "Principal matcha" products on Marukyu Koyamaen and sends a phone notification the moment any of them comes back in stock.

It checks every 5 minutes, runs for free on GitHub Actions, and keeps working when your computer is off.

Anyone is welcome to fork this and use it for themselves.

## How it works

1. A scheduled GitHub Actions workflow runs `check_stock.py`.
2. The script loads each product page and looks for the phrase the site shows when an item is sold out.
3. It compares the result to `state.json`, which stores what was in or out of stock on the previous run.
4. If a product flips from out of stock to in stock, it sends a push notification through [ntfy](https://ntfy.sh). You only get notified on a change, never on every run.
5. The workflow saves the updated `state.json` back to the repo for the next run.

## Setup (about 5 minutes)

### 1. Get the notification app

- Install **ntfy** on your phone: [iOS](https://apps.apple.com/us/app/ntfy/id1625396347) or [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
- Open the app, tap **+**, and subscribe to a topic.
- Pick a topic name nobody else would guess, for example `matcha-alerts-8f2k1x39`. ntfy topics are public to anyone who knows the name, so a simple name like `matcha` means strangers could read your alerts or send you fake ones.

### 2. Fork or create the repo

- Click **Fork** on this repo, or create your own and upload `check_stock.py`, `state.json`, and the workflow file at `.github/workflows/check-stock.yml`.
- On a fork, open the **Actions** tab and click the button to enable workflows. GitHub turns them off by default on forks.

### 3. Add your topic as a secret

- In your repo go to **Settings → Secrets and variables → Actions → New repository secret**
- Name: `NTFY_TOPIC`
- Value: the topic name from step 1

### 4. Let the workflow save its state

- Go to **Settings → Actions → General → Workflow permissions**
- Choose **Read and write permissions** and save.

### 5. Turn it on

- Open the **Actions** tab and select **Check matcha stock**.
- Click **Run workflow** once to test it.
- Open the run log. Each product should print its status, and most will say `out of stock` unless a restock just happened.
- After that it runs on its own every 5 minutes.

## When it fires

You get a high priority notification titled something like "🍵 Wako is back in stock!" with a tap-through link to the product page. If several products restock at once, you get a single notification listing all of them.

These items sell out fast, so before a restock happens:

- Register and log in at marukyu-koyamaen.co.jp. The site requires an account to buy ([register here](https://www.marukyu-koyamaen.co.jp/english/shop/account)).
- Save your payment and shipping info in your account so checkout takes seconds.

## Customizing

- **Products:** edit the `PRODUCTS` list in `check_stock.py`. Each entry is a name and a product page URL.
- **Sold out phrase:** if the site ever changes its wording, update `OUT_OF_STOCK_MARKER`. If that phrase stops matching, every product will look in stock, so check this first when you get a burst of false alerts.
- **Frequency:** change the `cron` line in the workflow file.

## Notes and limitations

- GitHub's free scheduled jobs are not precise. Expect a delay of roughly 1 to 10 minutes depending on GitHub's load.
- For faster checks, run the script on an always on machine such as a Raspberry Pi: `NTFY_TOPIC=your-topic python3 check_stock.py` on a loop or a 1 minute cron.
- The script treats a product page as in stock when the sold out phrase is missing. Some products come in multiple sizes, so it fires when any size becomes buyable.
- Please keep the 1 second pause between requests so the shop's server is not hammered.

## Troubleshooting

If a run fails while reading `state.json`, replace the file contents with `{}`. The next run rebuilds it.
