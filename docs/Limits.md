# Limits

Get account funds and limits.

```python
client.limits()
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

limits = client.limits()
result = limits.get("result", [{}])[0]
print(f"Cash Available: {result.get('openingCashLimit')}")
print(f"Margin Used: {result.get('utilizedMargin')}")
```

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "tradingLimit": 0,
        "openingCashLimit": 52926.40,
        "intradayPayin": 0,
        "collateralMargin": 47735.39,
        "creditForSell": 0,
        "adhocMargin": 0.000000,
        "utilizedMargin": 69.95,
        "blockedForPayout": 0.00,
        "utilizedSpanMargin": 0.00,
        "utilizedExposureMargin": 0.00
    }]
}
```

## Response Fields

| Field | Description |
|-------|-------------|
| tradingLimit | Max limit for trading |
| openingCashLimit | Cash at start of day |
| collateralMargin | Margin from pledged securities |
| utilizedMargin | Total margin used |
| utilizedSpanMargin | SPAN margin for derivatives |

[[Back to top]](#) [[Back to README]](../README.md)
