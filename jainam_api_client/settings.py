"""
Configuration and Constants for Jainam Lite API

Values from API documentation appendix.
"""

# Order Types
ORDER_TYPE_LIMIT = "LIMIT"
ORDER_TYPE_MARKET = "MARKET"
ORDER_TYPE_SL = "SL"       # Stop Loss
ORDER_TYPE_SLM = "SLM"     # Stop Loss Market

ORDER_TYPES = [ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET, ORDER_TYPE_SL, ORDER_TYPE_SLM]

# Product Types
PRODUCT_INTRADAY = "INTRADAY"   # Positions squared off same day
PRODUCT_LONGTERM = "LONGTERM"   # Delivery-based (CNC equivalent)
PRODUCT_MTF = "MTF"             # Margin Trading Facility

PRODUCTS = [PRODUCT_INTRADAY, PRODUCT_LONGTERM, PRODUCT_MTF]

# Holdings Product Types (for API requests)
HOLDINGS_PRODUCT_MAP = {
    "cnc": "LONGTERM",
    "mtf": "MTF",
    "mis": "INTRADAY",
}

# Exchanges
EXCHANGE_NSE = "NSE"
EXCHANGE_BSE = "BSE"
EXCHANGE_NFO = "NFO"
EXCHANGE_BFO = "BFO"
EXCHANGE_MCX = "MCX"
EXCHANGE_CDS = "CDS"
EXCHANGE_BCD = "BCD"
EXCHANGE_NCO = "NCO"
EXCHANGE_BCO = "BCO"

EXCHANGES = [
    EXCHANGE_NSE, EXCHANGE_BSE, EXCHANGE_NFO, EXCHANGE_BFO,
    EXCHANGE_MCX, EXCHANGE_CDS, EXCHANGE_BCD, EXCHANGE_NCO, EXCHANGE_BCO
]

# Transaction Types
TRANSACTION_BUY = "BUY"
TRANSACTION_SELL = "SELL"

TRANSACTION_TYPES = [TRANSACTION_BUY, TRANSACTION_SELL]

# Order Complexity
COMPLEXITY_REGULAR = "REGULAR"
COMPLEXITY_AMO = "AMO"       # After Market Order
COMPLEXITY_BO = "BO"         # Bracket Order
COMPLEXITY_CO = "CO"         # Cover Order

ORDER_COMPLEXITIES = [COMPLEXITY_REGULAR, COMPLEXITY_AMO, COMPLEXITY_BO, COMPLEXITY_CO]

# Order Validity
VALIDITY_DAY = "DAY"
VALIDITY_IOC = "IOC"  # Immediate or Cancel

VALIDITIES = [VALIDITY_DAY, VALIDITY_IOC]

# Order Statuses
ORDER_STATUS_OPEN = "OPEN"
ORDER_STATUS_COMPLETE = "COMPLETE"
ORDER_STATUS_REJECTED = "REJECTED"
ORDER_STATUS_CANCELLED = "CANCELLED"
ORDER_STATUS_PENDING = "PENDING"

# WebSocket Message Types
WS_TYPE_CONNECT = "c"           # Connection
WS_TYPE_HEARTBEAT = "h"         # Heartbeat
WS_TYPE_TICK = "t"              # Tick subscription
WS_TYPE_DEPTH = "d"             # Depth subscription
WS_TYPE_UNSUBSCRIBE = "u"       # Unsubscribe tick
WS_TYPE_UNSUBSCRIBE_DEPTH = "ud"  # Unsubscribe depth

# WebSocket Response Types
WS_RESP_CONNECT = "cf"          # Connection success
WS_RESP_TICK_ACK = "tk"         # Tick acknowledgement
WS_RESP_TICK_FEED = "tf"        # Tick feed
WS_RESP_DEPTH_ACK = "dk"        # Depth acknowledgement
WS_RESP_DEPTH_FEED = "df"       # Depth feed

# Rate Limits
RATE_LIMIT_GENERAL = 1800       # Per 15 minutes
RATE_LIMIT_WINDOW = 15 * 60     # 15 minutes in seconds
