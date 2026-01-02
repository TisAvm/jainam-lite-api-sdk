# Jainam Lite API Python SDK

A lightweight Python wrapper for the Jainam Lite Trading API.

[![Python](https://img.shields.io/badge/Python-3.8%20to%203.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Official API Docs**: https://protrade.jainam.in/open-apidocs/v2/index.html  

## Features

- 🔐 **SSO Authentication** with session caching
- 📊 **Order Management** - Place, modify, cancel orders
- 💼 **Portfolio** - Positions, holdings, square-off
- 💰 **Account** - Funds, limits, margins, profile
- 📈 **Market Data** - Contract master, symbol search
- ⚡ **WebSocket** - Real-time tick and depth data
- 🧪 **Auto-Login** - Selenium-based automated login for testing

---

## Installation

### pip install (from GitHub)

```bash
pip install git+https://github.com/TisAvm/jainam-lite-api-sdk.git
```

### Development install

```bash
git clone https://github.com/TisAvm/jainam-lite-api-sdk.git
cd jainam-lite-api-sdk
pip install -e .
```

---

## Quick Start

### 1. Set Up Credentials

Copy `.env.example` to `.env` and fill in your credentials:

```env
JAINAM_USER_ID=your_user_id
JAINAM_API_SECRET=your_api_secret
JAINAM_APP_CODE=your_app_code
```

### 2. Authentication

#### Option A: Interactive Login (Recommended)

```python
from jainam_api_client import SessionManager, interactive_login

# Prompts for authCode if no cached session
session = interactive_login()
api = session.get_api_client()

# Use the API
print(api.limits())
print(api.positions())
```

#### Option B: Use Cached Session

```python
from jainam_api_client import SessionManager

sm = SessionManager()
if sm.load_session() and sm.is_session_valid():
    api = sm.get_api_client()
    print("Using cached session")
else:
    print("Session expired. Run auto_login.py or interactive_login()")
```

#### Option C: Direct SSO Login

```python
from jainam_api_client import JainamAPI

client = JainamAPI()

# After user redirects back from Jainam login with authCode
client.login_with_sso(
    user_id="YOUR_USER_ID",
    auth_code="AUTH_CODE_FROM_REDIRECT",
    api_secret="YOUR_API_SECRET",
    app_code="YOUR_APP_CODE"
)
```

---

## Usage Examples

### Place Orders

```python
# Market order
response = client.place_market_order(
    exchange="NSE",
    instrument_id="14366",
    transaction_type="BUY",
    quantity=10
)

# Limit order
response = client.place_limit_order(
    exchange="NSE",
    instrument_id="14366",
    transaction_type="BUY",
    quantity=10,
    price="150.50"
)

# Full order with all options
response = client.place_order(
    exchange="NFO",
    instrument_id="40503",
    transaction_type="SELL",
    quantity=65,
    product="LONGTERM",         # INTRADAY, LONGTERM, MTF
    order_complexity="REGULAR", # REGULAR, AMO
    order_type="LIMIT",         # LIMIT, MARKET, SL, SLM
    price="250.00",
    validity="DAY",             # DAY, IOC
    order_tag="my_strategy"
)
```

### Modify & Cancel Orders

```python
# Modify order
client.modify_order(
    broker_order_id="250526000002881",
    quantity=20,
    price="155.00"
)

# Cancel order
client.cancel_order(broker_order_id="250526000002881")
```

### Order & Trade Reports

```python
# Order book (all orders)
orders = client.order_report()

# Trade book (executed trades)
trades = client.trade_report()

# Order history (state transitions)
history = client.order_history(broker_order_id="250526000002881")
```

### Portfolio

```python
# Get positions
positions = client.positions()

# Get holdings
holdings = client.holdings()  # Default: CNC/LONGTERM
holdings = client.holdings(product_type="mtf")

# Square off position
client.square_off([{
    "exchange": "NSE",
    "instrumentId": "14366",
    "transactionType": "SELL",
    "quantity": 10,
    "product": "LONGTERM",
    "orderComplexity": "REGULAR",
    "orderType": "MARKET",
    "validity": "DAY"
}])
```

### Account Information

```python
# Funds and limits
limits = client.limits()

# User profile
profile = client.profile()

# Margin required for an order
margin = client.margin_required(
    exchange="NSE",
    instrument_id="22",
    transaction_type="BUY",
    quantity=100,
    product="INTRADAY",
    order_type="MARKET"
)
```

### Contract Master

```python
# Download contract master
nse_contracts = client.contract_master("nse")
nfo_contracts = client.contract_master("nfo")

# Search for instruments
results = client.search_symbol(
    exchange="nfo",
    symbol="NIFTY",
    expiry="26DEC",
    option_type="CE",
    strike_price=24000
)
```

### WebSocket (Real-time Data)

```python
# Define callbacks
def on_message(msg):
    print(f"Tick: {msg}")

def on_error(error):
    print(f"Error: {error}")

# Set callbacks
client.on_message = on_message
client.on_error = on_error

# Subscribe to tick data
client.subscribe([
    {"exchange": "NSE", "token": "26000"},  # NIFTY 50
    {"exchange": "NSE", "token": "26009"}   # NIFTY BANK
])

# Subscribe to depth data (5-level market depth)
client.subscribe([
    {"exchange": "NFO", "token": "54957"}
], is_depth=True)

# Unsubscribe
client.unsubscribe([{"exchange": "NSE", "token": "26000"}])
```

---

## Testing

The SDK includes comprehensive integration tests with Selenium-based auto-login.

### Setup

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Configure credentials in .env (including TOTP for auto-login)
JAINAM_USER_PASSWORD=your_password
TOTP_TOKEN=your_totp_secret
```

### Run Tests

```bash
# Unified test - auto-login + test all APIs
python tests/test_all_apis.py

# Auto-login only (saves session to ~/.jainam_session.json)
python tests/auto_login.py

# Order placement test (WARNING: places REAL orders!)
python tests/test_place_order.py

# WebSocket test
python tests/test_websocket.py
```

### Test Output

| File | Description |
|------|-------------|
| `tests/test_output.txt` | Detailed test log |
| `tests/test_results.json` | JSON summary with raw API responses |
| `tests/order_test_output.txt` | Order test detailed log |
| `tests/order_test_results.json` | Order test results |

---

## API Reference

| Category | Method | Description |
|----------|--------|-------------|
| **Authentication** | | |
| | [`login_with_sso()`](docs/Session_init.md) | SSO vendor authentication |
| | `set_access_token()` | Set JWT token directly |
| | `logout()` | Clear session |
| **Orders** | | |
| | [`place_order()`](docs/Place_Order.md) | Place order (full options) |
| | `place_market_order()` | Quick market order |
| | `place_limit_order()` | Quick limit order |
| | [`modify_order()`](docs/Modify_Order.md) | Modify existing order |
| | [`cancel_order()`](docs/Cancel_Order.md) | Cancel order |
| **Order Info** | | |
| | [`order_report()`](docs/Order_report.md) | Get order book |
| | [`order_history()`](docs/Order_history.md) | Get order audit trail |
| | [`trade_report()`](docs/Trade_report.md) | Get trade book |
| **Portfolio** | | |
| | [`positions()`](docs/Positions.md) | Get open positions |
| | `square_off()` | Close positions |
| | [`holdings()`](docs/Holdings.md) | Get holdings |
| **Account** | | |
| | [`limits()`](docs/Limits.md) | Get funds/limits |
| | [`profile()`](docs/Profile.md) | Get user profile |
| | [`margin_required()`](docs/Margin.md) | Check margin |
| **Market Data** | | |
| | [`contract_master()`](docs/Contract_Master.md) | Download contract data |
| | `search_symbol()` | Search instruments |
| **WebSocket** | | |
| | [`subscribe()`](docs/WebSocket.md) | Subscribe to market data |
| | `unsubscribe()` | Unsubscribe |

---

## Constants

### Exchanges
| Code | Description |
|------|-------------|
| `NSE` | National Stock Exchange |
| `BSE` | Bombay Stock Exchange |
| `NFO` | NSE Futures & Options |
| `BFO` | BSE Futures & Options |
| `MCX` | Multi Commodity Exchange |
| `CDS` | Currency Derivatives |

### Products
| Code | Description |
|------|-------------|
| `INTRADAY` | Squared off same day |
| `LONGTERM` | Delivery/CNC |
| `MTF` | Margin Trading Facility |

### Order Types
| Code | Description |
|------|-------------|
| `LIMIT` | Limit order |
| `MARKET` | Market order |
| `SL` | Stop loss limit |
| `SLM` | Stop loss market |

### Validity
| Code | Description |
|------|-------------|
| `DAY` | Valid for the day |
| `IOC` | Immediate or Cancel |

---

## Session Management

The SDK provides `SessionManager` for automatic session caching:

```python
from jainam_api_client import SessionManager

sm = SessionManager()

# Session is cached to ~/.jainam_session.json
# Contains: access_token, checksum, login_time, user_id

# Check if session is valid (default: 8 hours)
if sm.load_session() and sm.is_session_valid():
    api = sm.get_api_client()
else:
    # Need to login again
    sm.login_with_authcode("NEW_AUTH_CODE")
```

---

## Rate Limits

| Type | Limit |
|------|-------|
| Orders | Unlimited |
| Other requests | 1800 per 15 minutes |

---

## Project Structure

```
jainam-lite-api-sdk/
├── jainam_api_client/
│   ├── __init__.py          # Package exports
│   ├── jainam_api.py         # Main API client
│   ├── session.py            # Session management
│   ├── rest.py               # REST client
│   ├── websocket.py          # WebSocket client
│   ├── exceptions.py         # Custom exceptions
│   ├── urls.py               # API endpoints
│   ├── settings.py           # Configuration
│   └── api/                  # API modules
│       ├── auth_api.py
│       ├── order_api.py
│       ├── modify_order_api.py
│       ├── cancel_order_api.py
│       ├── order_report_api.py
│       ├── order_history_api.py
│       ├── trade_report_api.py
│       ├── positions_api.py
│       ├── holdings_api.py
│       ├── funds_api.py
│       ├── margin_api.py
│       ├── profile_api.py
│       └── contract_master_api.py
├── tests/
│   ├── auto_login.py         # Selenium auto-login
│   ├── test_all_apis.py      # Unified API tests
│   ├── test_place_order.py   # Order placement test
│   ├── test_websocket.py     # WebSocket tests
│   └── requirements.txt      # Test dependencies
├── docs/                     # API documentation
├── .env.example              # Example environment config
├── setup.py                  # Package setup
└── README.md
```

---

## Support & Contributions

Feel free to open GitHub issues for:
- Bugs or unexpected API behavior
- Documentation improvements
- Feature requests
- Questions

Include request/response payloads when reporting issues.

## Contact

- **Email**: mishraaviralanand@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/tis-avm

---

## Disclaimer

This is an **unofficial SDK** and is not maintained by Jainam Broking Ltd.

---

## License

MIT License - see [LICENSE](LICENSE) for details.
