import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

logger = setup_logger("client")

BASE_URL = "https://demo-fapi.binance.com"
RECV_WINDOW = 5000  # milliseconds


class BinanceClientError(Exception):
    """Raised for non-2xx Binance API responses."""
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self.payload = payload
        msg = payload.get("msg", "Unknown API error")
        code = payload.get("code", "N/A")
        super().__init__(f"Binance API error {code}: {msg} (HTTP {status_code})")


class BinanceFuturesClient:
    """Lightweight wrapper around Binance USDT-M Futures Demo REST API."""

    def __init__(self, api_key: str, secret_key: str):
        if not api_key or not secret_key:
            raise ValueError("API key and secret key must not be empty.")
        self._api_key = api_key
        self._secret = secret_key.encode()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "X-MBX-APIKEY": self._api_key,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        logger.info("BinanceFuturesClient initialised (demo endpoint).")

    # ------------------------------------------------------------------ #
    # Private helpers                                                       #
    # ------------------------------------------------------------------ #

    def _timestamp(self) -> int:
        return int(time.time() * 1000)

    def _sign(self, params: dict) -> str:
        query = urlencode(params)
        signature = hmac.new(self._secret, query.encode(), hashlib.sha256).hexdigest()
        return signature

    def _build_signed_params(self, params: dict) -> dict:
        params["timestamp"] = self._timestamp()
        params["recvWindow"] = RECV_WINDOW
        params["signature"] = self._sign(params)
        return params

    # ------------------------------------------------------------------ #
    # Public request methods                                               #
    # ------------------------------------------------------------------ #

    def post(self, path: str, params: dict) -> dict:
        """Sign and POST to a private endpoint."""
        signed = self._build_signed_params(params)
        url = BASE_URL + path

        logger.debug(f"POST {url} | params (excl. signature): { {k: v for k, v in signed.items() if k != 'signature'} }")

        try:
            resp = self._session.post(url, data=signed, timeout=10)
        except requests.exceptions.ConnectionError as exc:
            logger.error(f"Network failure on POST {url}: {exc}")
            raise ConnectionError(f"Cannot reach Binance demo API: {exc}") from exc
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out: POST {url}")
            raise TimeoutError("Request to Binance timed out. Try again.")

        logger.debug(f"Response HTTP {resp.status_code}: {resp.text[:500]}")

        payload = resp.json()
        if not resp.ok:
            logger.error(f"API error {resp.status_code}: {payload}")
            raise BinanceClientError(resp.status_code, payload)

        return payload

    def get(self, path: str, params: dict | None = None) -> dict:
        """Sign and GET from a private endpoint."""
        params = params or {}
        signed = self._build_signed_params(params)
        url = BASE_URL + path

        logger.debug(f"GET {url} | params: { {k: v for k, v in signed.items() if k != 'signature'} }")

        try:
            resp = self._session.get(url, params=signed, timeout=10)
        except requests.exceptions.ConnectionError as exc:
            logger.error(f"Network failure on GET {url}: {exc}")
            raise ConnectionError(f"Cannot reach Binance demo API: {exc}") from exc
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out: GET {url}")
            raise TimeoutError("Request to Binance timed out. Try again.")

        logger.debug(f"Response HTTP {resp.status_code}: {resp.text[:500]}")

        payload = resp.json()
        if not resp.ok:
            logger.error(f"API error {resp.status_code}: {payload}")
            raise BinanceClientError(resp.status_code, payload)

        return payload
