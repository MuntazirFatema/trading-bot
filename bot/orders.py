from bot.client import BinanceFuturesClient
from bot.logging_config import setup_logger

logger = setup_logger("orders")

ORDER_ENDPOINT = "/fapi/v1/order"


def place_market_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float,
) -> dict:
    """
    Place a MARKET order on Binance Futures Demo.

    Args:
        client:   Authenticated BinanceFuturesClient.
        symbol:   Trading pair, e.g. 'BTCUSDT'.
        side:     'BUY' or 'SELL'.
        quantity: Number of contracts/coins.

    Returns:
        Raw response dict from Binance.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
    }
    logger.info(f"Placing MARKET order — {side} {quantity} {symbol}")
    response = client.post(ORDER_ENDPOINT, params)
    logger.info(f"MARKET order placed. orderId={response.get('orderId')}, status={response.get('status')}")
    return response


def place_limit_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:
    """
    Place a LIMIT order on Binance Futures Demo.

    Args:
        client:        Authenticated BinanceFuturesClient.
        symbol:        Trading pair, e.g. 'BTCUSDT'.
        side:          'BUY' or 'SELL'.
        quantity:      Number of contracts/coins.
        price:         Limit price.
        time_in_force: Default GTC (Good Till Cancelled).

    Returns:
        Raw response dict from Binance.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": time_in_force,
    }
    logger.info(f"Placing LIMIT order — {side} {quantity} {symbol} @ {price}")
    response = client.post(ORDER_ENDPOINT, params)
    logger.info(f"LIMIT order placed. orderId={response.get('orderId')}, status={response.get('status')}")
    return response


def print_order_summary(response: dict) -> None:
    """Pretty-print the key fields from a Binance order response."""
    print("\n" + "=" * 55)
    print("           ORDER PLACED SUCCESSFULLY")
    print("=" * 55)

    fields = [
        ("Order ID",       response.get("orderId", "N/A")),
        ("Client Order ID",response.get("clientOrderId", "N/A")),
        ("Symbol",         response.get("symbol", "N/A")),
        ("Side",           response.get("side", "N/A")),
        ("Type",           response.get("type", "N/A")),
        ("Quantity",       response.get("origQty", "N/A")),
        ("Price",          response.get("price", "N/A")),
        ("Avg Fill Price", response.get("avgPrice", "N/A")),
        ("Status",         response.get("status", "N/A")),
        ("Time in Force",  response.get("timeInForce", "N/A")),
        ("Created At (ms)",response.get("updateTime", "N/A")),
    ]

    for label, value in fields:
        print(f"  {label:<20}: {value}")

    print("=" * 55 + "\n")
