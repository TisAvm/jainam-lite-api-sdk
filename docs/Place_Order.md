# Place Order

Place a new order.

```python
client.place_order(
    exchange="",
    instrument_id="",
    transaction_type="",
    quantity=0,
    product="LONGTERM",
    order_complexity="REGULAR",
    order_type="LIMIT",
    price="",
    validity="DAY",
    sl_trigger_price="",
    trailing_sl_amount="",
    disclosed_quantity=0,
    market_protection_percent="",
    api_order_source="",
    algo_id="",
    order_tag=""
)
```

## Example

```python
from jainam_api_client import JainamAPI

# Initialize and authenticate
client = JainamAPI()
client.login_with_sso(user_id="", auth_code="", api_secret="", app_code="")

try:
    # Place a limit order
    response = client.place_order(
        exchange="NSE",
        instrument_id="14366",
        transaction_type="BUY",
        quantity=10,
        product="LONGTERM",
        order_complexity="REGULAR",
        order_type="LIMIT",
        price="6.3",
        validity="DAY"
    )
    print(f"Order placed: {response}")
except Exception as e:
    print(f"Error: {e}")
```

## Quick Methods

```python
# Market order
client.place_market_order(
    exchange="NSE",
    instrument_id="14366",
    transaction_type="BUY",
    quantity=10
)

# Limit order
client.place_limit_order(
    exchange="NSE",
    instrument_id="14366",
    transaction_type="BUY",
    quantity=10,
    price="6.3"
)
```

## Parameters

| Name | Description | Type |
|------|-------------|------|
| *exchange* | NSE, BSE, NFO, BFO, MCX, CDS | Str (required) |
| *instrument_id* | Unique instrument ID from contract master | Str (required) |
| *transaction_type* | BUY, SELL | Str (required) |
| *quantity* | Order quantity | Int (required) |
| *product* | INTRADAY, LONGTERM, MTF | Str (default: LONGTERM) |
| *order_complexity* | REGULAR, AMO | Str (default: REGULAR) |
| *order_type* | LIMIT, MARKET, SL, SLM | Str (default: LIMIT) |
| *price* | Order price | Str (required for LIMIT) |
| *validity* | DAY, IOC | Str (default: DAY) |
| *sl_trigger_price* | Stop loss trigger price | Str (optional) |
| *trailing_sl_amount* | Trailing stop loss amount | Str (optional) |
| *disclosed_quantity* | Disclosed quantity | Int (optional) |
| *market_protection_percent* | Market protection % | Str (optional) |
| *api_order_source* | API source identifier | Str (optional) |
| *algo_id* | Algorithm ID (max 12 chars) | Str (optional) |
| *order_tag* | Custom tag (max 50 chars) | Str (optional) |

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "requestTime": "26-May-2025 11:42:10",
        "brokerOrderId": "250526000002697"
    }]
}
```

## HTTP Response Codes

| Status | Description |
|--------|-------------|
| *200* | Order placed successfully |
| *400* | Invalid or missing parameters |
| *403* | Invalid session |
| *429* | Too many requests |
| *500* | Unexpected error |

[[Back to top]](#) [[Back to README]](../README.md)
