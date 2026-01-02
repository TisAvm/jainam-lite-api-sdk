# Margin Required

Check margin required for an order.

```python
client.margin_required(
    exchange="",
    instrument_id="",
    transaction_type="",
    quantity=0,
    product="",
    order_type="MARKET",
    price=None
)
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

margin = client.margin_required(
    exchange="NSEEQ",
    instrument_id="22",
    transaction_type="BUY",
    quantity=1,
    product="INTRADAY",
    order_type="MARKET"
)
result = margin.get("result", [{}])[0]
print(f"Margin Required: {result.get('currentOrderMargin')}")
```

## Parameters

| Name | Description | Type |
|------|-------------|------|
| *exchange* | NSEEQ, BSEEQ, etc. | Str (required) |
| *instrument_id* | Instrument ID | Str (required) |
| *transaction_type* | BUY, SELL | Str (required) |
| *quantity* | Quantity | Int (required) |
| *product* | INTRADAY, LONGTERM | Str (required) |
| *order_type* | LIMIT, MARKET | Str (default: MARKET) |
| *price* | Price for limit orders | Str (optional) |

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "status": "Ok",
        "message": "Success",
        "totalCashAvailable": "52926",
        "preOrderMargin": "",
        "postOrderMargin": "183.65",
        "currentOrderMargin": "113.70",
        "rmsValidationCheck": "",
        "fundShort": ""
    }]
}
```

[[Back to top]](#) [[Back to README]](../README.md)
