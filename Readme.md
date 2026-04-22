# 🤖 Binance Futures Demo Trading Bot

A command-line trading bot for placing **MARKET** and **LIMIT** orders on the [Binance Futures Demo](https://demo-fapi.binance.com) (USDT-M).

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # HMAC signing + HTTP requests
│   ├── orders.py          # place_market_order / place_limit_order
│   ├── validators.py      # Input validation
│   └── logging_config.py  # File + console logger
├── cli.py                 # Argparse entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/trading-bot.git
cd trading-bot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set API credentials

You can pass credentials via environment variables (recommended) or CLI flags.

**Environment variables (Linux/macOS):**
```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_SECRET_KEY="your_secret_key_here"
```

**Windows (CMD):**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_SECRET_KEY=your_secret_key_here
```

Or pass them directly with `--api-key` and `--secret-key` flags (see below).

---

## 🚀 Run Examples

### Place a MARKET BUY order

```bash
python cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

### Place a LIMIT SELL order

```bash
python cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.001 \
  --price 50000
```

### Pass credentials inline (alternative to env vars)

```bash
python cli.py \
  --symbol ETHUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.01 \
  --api-key YOUR_API_KEY \
  --secret-key YOUR_SECRET_KEY
```

---

## 📋 CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `--symbol` | ✅ | Trading pair (e.g. `BTCUSDT`) |
| `--side` | ✅ | `BUY` or `SELL` |
| `--type` | ✅ | `MARKET` or `LIMIT` |
| `--quantity` | ✅ | Order quantity (float) |
| `--price` | ⚠️ LIMIT only | Limit price (float) |
| `--api-key` | optional | Overrides `BINANCE_API_KEY` env var |
| `--secret-key` | optional | Overrides `BINANCE_SECRET_KEY` env var |

---

## 📝 Logs

Logs are written to `logs/trading_bot_YYYYMMDD.log`.

Each run logs:
- Validated input parameters
- Full API request details (params, endpoint)
- Raw API response
- Any errors (validation, API, network, timeout)

---

## 🛡️ Error Handling

| Error Type | Handled? | Behaviour |
|---|---|---|
| Invalid input (bad side/type/qty) | ✅ | Prints validation error, exits cleanly |
| API error (e.g. wrong symbol) | ✅ | Prints Binance error code + message |
| Network failure | ✅ | Prints connection error, exits cleanly |
| Request timeout | ✅ | Prints timeout message, exits cleanly |

---

## 📌 Notes

- This bot targets the **Binance Futures Demo** environment only (`https://demo-fapi.binance.com`). No real funds are used.
- LIMIT orders default to `timeInForce=GTC` (Good Till Cancelled).
- Requires Python 3.10+.