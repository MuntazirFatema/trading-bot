#!/usr/bin/env python3
"""
Trading Bot CLI
---------------
Entry point for placing Binance Futures Demo orders from the command line.

Usage examples:
  python cli.py --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.001
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT  --quantity 0.001 --price 50000
"""

import argparse
import os
import sys

from bot.client import BinanceFuturesClient, BinanceClientError
from bot.logging_config import setup_logger
from bot.orders import place_market_order, place_limit_order, print_order_summary
from bot.validators import validate_all, ValidationError

logger = setup_logger("cli")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Simplified Binance Futures Demo Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--symbol", required=True,
        help="Trading pair symbol (e.g. BTCUSDT)"
    )
    parser.add_argument(
        "--side", required=True,
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type", dest="order_type", required=True,
        help="Order type: MARKET or LIMIT"
    )
    parser.add_argument(
        "--quantity", required=True, type=float,
        help="Order quantity (e.g. 0.001)"
    )
    parser.add_argument(
        "--price", type=float, default=None,
        help="Limit price (required for LIMIT orders)"
    )
    parser.add_argument(
        "--api-key", default=None,
        help="Binance API key (or set BINANCE_API_KEY env var)"
    )
    parser.add_argument(
        "--secret-key", default=None,
        help="Binance secret key (or set BINANCE_SECRET_KEY env var)"
    )

    return parser.parse_args()


def get_credentials(args: argparse.Namespace) -> tuple[str, str]:
    """Resolve API credentials: CLI args take precedence over env vars."""
    api_key = args.api_key or os.environ.get("BINANCE_API_KEY", "")
    secret_key = args.secret_key or os.environ.get("BINANCE_SECRET_KEY", "")

    if not api_key:
        logger.error("No API key provided.")
        print("[ERROR] Provide --api-key or set BINANCE_API_KEY environment variable.")
        sys.exit(1)

    if not secret_key:
        logger.error("No secret key provided.")
        print("[ERROR] Provide --secret-key or set BINANCE_SECRET_KEY environment variable.")
        sys.exit(1)

    return api_key, secret_key


def main() -> None:
    args = parse_args()

    # ── Credentials ──────────────────────────────────────────────────────
    api_key, secret_key = get_credentials(args)

    # ── Validate inputs ───────────────────────────────────────────────────
    try:
        params = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as exc:
        logger.error(f"Validation failed: {exc}")
        print(f"[VALIDATION ERROR] {exc}")
        sys.exit(1)

    # ── Initialise client ─────────────────────────────────────────────────
    try:
        client = BinanceFuturesClient(api_key=api_key, secret_key=secret_key)
    except ValueError as exc:
        logger.error(f"Client init failed: {exc}")
        print(f"[CONFIG ERROR] {exc}")
        sys.exit(1)

    # ── Place order ───────────────────────────────────────────────────────
    try:
        if params["order_type"] == "MARKET":
            response = place_market_order(
                client=client,
                symbol=params["symbol"],
                side=params["side"],
                quantity=params["quantity"],
            )
        else:  # LIMIT
            response = place_limit_order(
                client=client,
                symbol=params["symbol"],
                side=params["side"],
                quantity=params["quantity"],
                price=params["price"],
            )
    except BinanceClientError as exc:
        logger.error(f"Binance API returned an error: {exc}")
        print(f"\n[API ERROR] {exc}")
        sys.exit(1)
    except ConnectionError as exc:
        logger.error(f"Network error: {exc}")
        print(f"\n[NETWORK ERROR] {exc}")
        sys.exit(1)
    except TimeoutError as exc:
        logger.error(f"Timeout: {exc}")
        print(f"\n[TIMEOUT] {exc}")
        sys.exit(1)

    # ── Print summary ─────────────────────────────────────────────────────
    print_order_summary(response)
    logger.info("Order workflow completed successfully.")


if __name__ == "__main__":
    main()