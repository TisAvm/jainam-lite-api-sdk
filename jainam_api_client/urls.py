"""
API URL Constants for Jainam Lite API
"""

# Base URLs
BASE_URL = "https://protrade.jainam.in/"
WEBSOCKET_URL = "wss://ws.jainam.in/NorenWSTP/"

# Authentication
SSO_VENDOR_DETAILS = "omt/auth/sso/vendor/getUserDetails"

# Order Management
PLACE_ORDER = "omt/api-order-rest/v1/orders/placeorder"
ORDER_BOOK = "omt/api-order-rest/v1/orders/book"
ORDER_HISTORY = "omt/api-order-rest/v1/orders/history"
MODIFY_ORDER = "omt/api-order-rest/v1/orders/modify"
CANCEL_ORDER = "omt/api-order-rest/v1/orders/cancel"
TRADE_BOOK = "omt/api-order-rest/v1/orders/trades"
CHECK_MARGIN = "omt/od-rest-api/v1/orders/checkMargin"

# Portfolio
HOLDINGS = "omt/api-order-rest/v1/holdings/{product_type}"
POSITIONS = "omt/api-order-rest/v1/positions"
SQUARE_OFF = "omt/api-order-rest/v1/orders/positions/sqroff"

# Account
LIMITS = "omt/api-order-rest/v1/limits/"
PROFILE = "omt/api-order-rest/v1/profile/"

# WebSocket Session
CREATE_WS_SESSION = "api/client-rest/profile/createWsSess"
INVALIDATE_WS_SESSION = "api/client-rest/profile/invalidateWsSess"

# Contract Master - JSON format
CONTRACT_MASTER_JSON = "contract/json/{exchange}"

# Contract Master Download URLs (direct links)
CONTRACT_URLS = {
    "nse": f"{BASE_URL}contract/json/nse",
    "nfo": f"{BASE_URL}contract/json/nfo",
    "bse": f"{BASE_URL}contract/json/bse",
    "bfo": f"{BASE_URL}contract/json/bfo",
    "mcx": f"{BASE_URL}contract/json/mcx",
    "cds": f"{BASE_URL}contract/json/cds",
    "bcd": f"{BASE_URL}contract/json/bcd",
    "indices": f"{BASE_URL}contract/json/indices",
}
