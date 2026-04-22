from bot.logging_config import setup_logger

logger = setup_logger("validators")

SUPPORTED_ORDER_TYPES = {"MARKET", "LIMIT"}
SUPPORTED_SIDES = {"BUY", "SELL"}


class ValidationError(ValueError):
    """Raised when user-supplied trading parameters fail validation."""
    pass


def validate_symbol(symbol: str) -> str:
    """Normalise and basic-validate a trading symbol."""
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string.")
    symbol = symbol.upper().strip()
    if len(symbol) < 3:
        raise ValidationError(f"Symbol '{symbol}' looks too short to be valid.")
    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    """Ensure side is BUY or SELL."""
    side = side.upper().strip()
    if side not in SUPPORTED_SIDES:
        raise ValidationError(
            f"Invalid side '{side}'. Must be one of: {', '.join(SUPPORTED_SIDES)}"
        )
    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    """Ensure order type is MARKET or LIMIT."""
    order_type = order_type.upper().strip()
    if order_type not in SUPPORTED_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(SUPPORTED_ORDER_TYPES)}"
        )
    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity: float) -> float:
    """Ensure quantity is a positive number."""
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity must be a number, got: {quantity!r}")
    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than 0, got: {quantity}")
    logger.debug(f"Quantity validated: {quantity}")
    return quantity


def validate_price(price: float | None, order_type: str) -> float | None:
    """Price is required for LIMIT orders, must be positive."""
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders. Use --price.")
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValidationError(f"Price must be a number, got: {price!r}")
        if price <= 0:
            raise ValidationError(f"Price must be greater than 0, got: {price}")
        logger.debug(f"Price validated: {price}")
        return price
    # MARKET orders don't need price
    if price is not None:
        logger.warning("Price argument is ignored for MARKET orders.")
    return None


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict:
    """Run all validations and return a clean params dict."""
    return {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
        "price": validate_price(price, order_type.upper()),
    }