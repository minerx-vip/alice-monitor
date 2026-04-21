# Alice Protocol Mining Monitor

A public, read-only dashboard that shows per-epoch reward distribution across
all wallets on the Alice Protocol mining network for the last 24 hours.

Live data is pulled from the public indexer at
[`aliceprotocol.org/api/indexer/epochs`](https://aliceprotocol.org/api/indexer/epochs?limit=30)
and committed to the repo every ~10 minutes by a GitHub Action. The page
itself is a single static HTML file and runs entirely in the browser — no
server, no tracking, no dependencies.

## Features

- **Transposed epoch grid** — rows are wallets, columns are epochs, cells
  show reward (colored intensity) or shard count.
- **Last 24 hours** window by default. Adjust with `?hours=48` (max 168).
- **Top-N by reward** — default top 50. Use `?top=200` or `?top=all` to
  show more.
- **Watch your own wallets** — add any addresses with optional notes in the
  "My Wallets" panel. They're pinned to the top, highlighted, and summed in
  the hero card. List is saved in your browser's `localStorage` (private to
  you — never uploaded anywhere).
- **Share a watchlist** via URL:
  `?watch=a2v4...QNAgPHyDR|GPU0,a2xpC3...EQBniTc1P|GPU1` — opening the link
  prompts to merge into the local list.
- **Import/Export JSON** for moving your watchlist across devices.

## Project layout

```
index.html                          # single-page dashboard (all rendering in browser)
data/epochs.json                    # committed data file, updated by the cron
scripts/fetch_epochs.py             # stdlib-only fetcher
.github/workflows/update.yml        # cron: pull API → merge → commit
.github/workflows/pages.yml         # deploy repo to GitHub Pages on push
```

## Deploying your own copy

1. **Fork / create** a public repo with these files.
2. In your repo's **Settings → Actions → General**, make sure "Workflow
   permissions" is set to **Read and write permissions** (so the cron can
   commit `data/epochs.json` back to the repo).
3. In **Settings → Pages**, set **Source** to **GitHub Actions**.
4. Push to `main`. Two workflows will run:
   - `Update epoch data` — fetches the API and commits the JSON.
   - `Deploy to GitHub Pages` — publishes the site.
5. Your dashboard will be live at
   `https://<your-username>.github.io/<repo-name>/`.

The update job runs every 10 minutes (GitHub's cron is best-effort, so
expect occasional drift). You can also trigger it manually from the Actions
tab with **Run workflow**.

## Privacy

- The dashboard is fully client-side; your watchlist lives in browser
  `localStorage` under the key `alice_monitor_watchlist`. It is **never
  transmitted**.
- The only network calls from the page are (a) loading `data/epochs.json`
  from the same origin and (b) loading Tailwind from the Tailwind CDN.

## Local preview

```
cd alice-monitor-public
python3 -m http.server 8000
# open http://localhost:8000
```

Seed `data/epochs.json` by running the fetcher locally:

```
python3 scripts/fetch_epochs.py
```

## License

MIT
