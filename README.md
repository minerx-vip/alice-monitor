# Alice Protocol Mining Monitor

[English](#english) · [中文](#中文)

在线访问：**https://minerx-vip.github.io/alice-monitor/**

---

## 中文

一个公开、只读的 Alice Protocol 挖矿监控面板，展示**最近 24 小时**全网所有钱包在每个纪元（epoch）上的奖励分布。

数据来自官方公开接口
[`aliceprotocol.org/api/indexer/epochs`](https://aliceprotocol.org/api/indexer/epochs?limit=30)，
由 GitHub Actions 每约 10 分钟拉取一次并提交到仓库。页面本身是一个纯静态
HTML 文件，**完全运行在浏览器里** —— 没有服务器、没有埋点、没有任何外部依赖。

### 功能

- **纪元矩阵视图** —— 行是钱包，列是纪元，格子显示该纪元的奖励（颜色深浅表示金额）或 shard 数。
- **窗口默认 24 小时**，可通过 URL 参数调整：`?hours=48`（最大 168）。
- **按奖励排序 Top-N** —— 默认显示 Top 200。`?top=500` 或 `?top=all` 可调。
- **我的钱包（追踪功能）** —— 在 "👛 My Wallets" 面板添加任意数量的钱包地址并附上备注。被追踪的钱包会：
  - 置顶，黄色高亮，带 ★ 标
  - 在页面顶部 Hero 卡片里汇总：窗口期总奖励、命中纪元数、占奖池百分比
  - 即使在窗口期内 0 奖励也会显示（方便确认 "在挖但没中奖"）
  - 列表保存在你浏览器的 `localStorage` 中，**只在你这台浏览器上存在，从不上传**
- **分享钱包列表** —— 用 URL：`?watch=地址1|备注1,地址2|备注2`。对方打开链接时会被询问是否合并进本地列表。
- **JSON 导入/导出** —— 换设备时用来迁移追踪列表。

### 目录结构

```
index.html                          # 单页面仪表盘，所有渲染在浏览器完成
data/epochs.json                    # 纪元数据，由定时任务写入
scripts/fetch_epochs.py             # 拉取脚本（仅用 Python 标准库）
.github/workflows/update.yml        # 定时任务：拉 API → 合并 → 提交
.github/workflows/pages.yml         # push 后自动部署到 GitHub Pages
```

### 自己部署一份

1. **Fork 或新建** 一个公开仓库，把这些文件放进去。
2. 仓库 **Settings → Actions → General → Workflow permissions** 切到 **Read and write permissions**，以便定时任务能把 `data/epochs.json` 提交回仓库。
3. **Settings → Pages → Source** 选 **GitHub Actions**。
4. 推送到 `main`，两个 workflow 会跑起来：
   - `Update epoch data` —— 拉取 API 并提交 JSON
   - `Deploy to GitHub Pages` —— 发布站点
5. 站点地址：`https://<你的用户名>.github.io/<仓库名>/`

定时任务每 10 分钟跑一次（GitHub 的 cron 是尽力而为，偶尔会漂移几分钟）。也可以在 Actions 页面手动点 **Run workflow** 立即触发。

### 隐私说明

- 面板**完全客户端运行**。你的追踪钱包列表保存在浏览器 `localStorage` 的 `alice_monitor_watchlist` 键下，**从不向任何服务器发送**。
- 页面对外的网络请求只有两个：
  1. 从同源加载 `data/epochs.json`
  2. 从 Tailwind CDN 加载样式库

### 本地预览

```bash
cd alice-monitor-public
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

首次本地预览前，先跑一次拉取脚本生成数据：

```bash
python3 scripts/fetch_epochs.py
```

### 许可

MIT

---

## English

A public, read-only dashboard that shows per-epoch reward distribution across
all wallets on the Alice Protocol mining network for the last 24 hours.

Live data is pulled from the public indexer at
[`aliceprotocol.org/api/indexer/epochs`](https://aliceprotocol.org/api/indexer/epochs?limit=30)
and committed to the repo every ~10 minutes by a GitHub Action. The page
itself is a single static HTML file and runs entirely in the browser — no
server, no tracking, no dependencies.

### Features

- **Transposed epoch grid** — rows are wallets, columns are epochs, cells
  show reward (colored intensity) or shard count.
- **Last 24 hours** window by default. Adjust with `?hours=48` (max 168).
- **Top-N by reward** — default top 200. Use `?top=500` or `?top=all` to
  show more.
- **Watch your own wallets** — add any addresses with optional notes in the
  "My Wallets" panel. They're pinned to the top, highlighted, and summed in
  the hero card. List is saved in your browser's `localStorage` (private to
  you — never uploaded anywhere).
- **Share a watchlist** via URL:
  `?watch=a2v4...QNAgPHyDR|GPU0,a2xpC3...EQBniTc1P|GPU1` — opening the link
  prompts to merge into the local list.
- **Import/Export JSON** for moving your watchlist across devices.

### Project layout

```
index.html                          # single-page dashboard (all rendering in browser)
data/epochs.json                    # committed data file, updated by the cron
scripts/fetch_epochs.py             # stdlib-only fetcher
.github/workflows/update.yml        # cron: pull API → merge → commit
.github/workflows/pages.yml         # deploy repo to GitHub Pages on push
```

### Deploying your own copy

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

### Privacy

- The dashboard is fully client-side; your watchlist lives in browser
  `localStorage` under the key `alice_monitor_watchlist`. It is **never
  transmitted**.
- The only network calls from the page are (a) loading `data/epochs.json`
  from the same origin and (b) loading Tailwind from the Tailwind CDN.

### Local preview

```bash
cd alice-monitor-public
python3 -m http.server 8000
# open http://localhost:8000
```

Seed `data/epochs.json` by running the fetcher locally:

```bash
python3 scripts/fetch_epochs.py
```

### License

MIT
