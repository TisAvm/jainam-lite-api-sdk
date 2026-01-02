# WebSocket

Real-time market data streaming.

```python
client.subscribe(instruments, is_depth=False)
client.unsubscribe(instruments, is_depth=False)
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.login_with_sso(
    user_id="DK2200295",
    auth_code="your_auth",
    api_secret="your_secret",
    app_code="your_app_code"
)

# Define callbacks
def on_message(message):
    print(message)

def on_error(error):
    print(f"Error: {error}")

def on_close(message):
    print(f"Closed: {message}")

def on_open():
    print("Connected!")

# Set callbacks
client.on_message = on_message
client.on_error = on_error
client.on_close = on_close
client.on_open = on_open

# Subscribe to tick data
client.subscribe([
    {"exchange": "NSE", "token": "26000"},  # NIFTY 50
    {"exchange": "NSE", "token": "26009"}   # NIFTY BANK
])

# Subscribe to depth data (5-level)
client.subscribe([
    {"exchange": "NFO", "token": "54957"}
], is_depth=True)

# Unsubscribe
client.unsubscribe([{"exchange": "NSE", "token": "26000"}])
```

## Parameters

| Name | Description | Type |
|------|-------------|------|
| *instruments* | List of {exchange, token} dicts | List (required) |
| *is_depth* | Subscribe to depth data | Bool (default: False) |

## Tick Data Response

```json
{"t": "tf", "e": "NFO", "tk": "54957", "lp": "84.20", "pc": "99.53", "ft": "1658911102"}
```

| Field | Description |
|-------|-------------|
| t | Type (tf=tick feed) |
| e | Exchange |
| tk | Token |
| lp | Last traded price |
| pc | Percent change |
| v | Volume |
| o | Open |
| h | High |
| l | Low |
| c | Close |
| oi | Open interest |

## Depth Data Response

```json
{
    "t": "df",
    "e": "NFO",
    "tk": "54957",
    "bp1": "84.30", "sp1": "84.50",
    "bq1": "1500", "sq1": "350",
    "bp2": "84.25", "sp2": "84.55",
    ...
}
```

| Field | Description |
|-------|-------------|
| bp1-bp5 | Bid prices (5 levels) |
| sp1-sp5 | Ask prices (5 levels) |
| bq1-bq5 | Bid quantities |
| sq1-sq5 | Ask quantities |
| tbq | Total buy quantity |
| tsq | Total sell quantity |

## Connection

- URL: `wss://ws.jainam.in/NorenWSTP/`
- Session token is double SHA-256 hashed
- Heartbeat should be sent every 50 seconds

[[Back to top]](#) [[Back to README]](../README.md)
