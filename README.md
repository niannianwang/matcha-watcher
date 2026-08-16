# Marukyu Koyamaen Matcha Restock Watcher

Watches all 11 "Principal matcha" products and pushes an urgent phone
notification the moment any of them come back in stock.

Checks every 5 minutes, runs for free on GitHub, works even when your
computer is off.

## Setup (~5 minutes)

### 1. Get the notification app
- Install **ntfy** on your phone: [iOS](https://apps.apple.com/us/app/ntfy/id1625396347) / [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
- Open the app, tap **+** to subscribe to a topic.
- Pick a **random, hard-to-guess topic name** (e.g. `matcha-alerts-8f2k1x39`) —
  anyone who knows this name can also see/send notifications to it, since
  ntfy topics aren't private by default. Subscribe to that exact name.

### 2. Create a GitHub repo
- Go to [github.com/new](https://github.com/new), create a new **public or
  private** repo (e.g. `matcha-watcher`).
- Upload all the files from this folder (`check_stock.py`,
  `state.json`, and the `.github/workflows/check-stock.yml` folder) —
  easiest way is drag-and-drop on the GitHub "Add file → Upload files" page,
  making sure the workflow file lands at `.github/workflows/check-stock.yml`.

### 3. Add your ntfy topic as a secret
- In your new repo: **Settings → Secrets and variables → Actions → New repository secret**
- Name: `NTFY_TOPIC`
- Value: the topic name you picked in step 1 (e.g. `matcha-alerts-8f2k1x39`)

### 4. Turn it on
- Go to the **Actions** tab of your repo → you should see "Check matcha stock".
- Click into it and click **Run workflow** once to test it manually.
- Check the run log — it should print each product's status
  (`out of stock` for all of them right now, most likely).
- After that, it runs automatically every 5 minutes via the schedule.

### 5. When it fires
You'll get a push notification titled something like "🍵 Wako is back in
stock!" with a tap-through link straight to the product page. Since you
mentioned it sells out fast, it's worth:
- Making sure you're already **registered and logged in** to
  marukyu-koyamaen.co.jp ahead of time (the site requires an account to
  buy — [register here](https://www.marukyu-koyamaen.co.jp/english/shop/account)).
- Keeping your payment/shipping info saved in your account so checkout is fast.

## Notes / limitations
- GitHub's free scheduled jobs aren't millisecond-precise — expect anywhere
  from ~1–10 minutes of delay depending on GitHub's load, not guaranteed
  exactly every 5 minutes.
- If you want faster checks, you could self-host this script instead (e.g.
  a Raspberry Pi or any always-on machine with cron every 1 minute) — the
  same `check_stock.py` works standalone, just run
  `NTFY_TOPIC=your-topic python3 check_stock.py` on a loop.
- The script currently checks whether the *whole product page* has no sold
  out marker — some products sell multiple sizes, and this triggers when
  *any* size is buyable again.
