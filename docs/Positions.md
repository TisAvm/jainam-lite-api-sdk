# Positions

Get open positions.

```python
client.positions()
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

positions = client.positions()
for pos in positions.get("result", []):
    print(f"{pos['tradingSymbol']}: {pos['netQuantity']} @ {pos['netAveragePrice']}")
```

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "instrumentId": "20776",
        "tradingSymbol": "BHAGYANGR-EQ",
        "formattedInstrumentName": "BHAGYANGR",
        "exchange": "NSE",
        "product": "LONGTERM",
        "netQuantity": 1,
        "netAveragePrice": 78.14,
        "overnightQuantity": 0,
        "overnightPrice": 0.00,
        "buyQuantity": 1,
        "sellQuantity": 0,
        "daySellQuantity": 0,
        "dayBuyQuantity": 1,
        "dayBuyPrice": 78.14,
        "daySellPrice": 0.00,
        "previousDayClose": 78.33,
        "realizedPnl": 0
    }]
}
```

## Square Off

```python
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

[[Back to top]](#) [[Back to README]](../README.md)
