# Modify Order

Modify an existing order.

```python
client.modify_order(
    broker_order_id="",
    quantity=None,
    order_type=None,
    price=None,
    sl_trigger_price=None,
    validity=None,
    disclosed_quantity=None,
    market_protection_percent=None,
    trailing_sl_amount=None
)
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

# Modify price and quantity
response = client.modify_order(
    broker_order_id="250526000002881",
    quantity=20,
    price="6.5"
)
```

## Parameters

| Name | Description | Type |
|------|-------------|------|
| *broker_order_id* | Order ID to modify | Str (required) |
| *quantity* | New quantity | Int (optional) |
| *order_type* | LIMIT, MARKET, SL, SLM | Str (optional) |
| *price* | New price | Str (optional) |
| *sl_trigger_price* | New trigger price | Str (optional) |
| *validity* | DAY, IOC | Str (optional) |
| *disclosed_quantity* | New disclosed qty | Str (optional) |
| *market_protection_percent* | New protection % | Str (optional) |
| *trailing_sl_amount* | New trailing SL | Str (optional) |

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "brokerOrderId": "250526000002881",
        "requestTime": "26-May-2025 13:11:34"
    }]
}
```

[[Back to top]](#) [[Back to README]](../README.md)
