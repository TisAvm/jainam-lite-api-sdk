# Trade Report

Get trade book (executed trades).

```python
client.trade_report()
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

trades = client.trade_report()
for trade in trades.get("result", []):
    print(f"{trade['tradingSymbol']}: {trade['filledQuantity']} @ {trade['tradedPrice']}")
```

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "clientId": "DK2200295",
        "placedBy": "DK2200295",
        "brokerOrderId": "250526000005634",
        "exchangeOrderId": "1100000067912030",
        "exchangeTradeId": "207745115",
        "formattedInstrumentName": "IDEA",
        "tradingSymbol": "IDEA-EQ",
        "instrumentId": "14366",
        "exchange": "NSE",
        "transactionType": "BUY",
        "product": "LONGTERM",
        "orderComplexity": "REGULAR",
        "orderType": "MARKET",
        "validity": "DAY",
        "tradedPrice": 6.95,
        "filledQuantity": 1,
        "orderTime": "2025-05-26 14:27:43",
        "fillTimestamp": "2025-05-26 14:27:43"
    }]
}
```

## Response Fields

| Field | Description |
|-------|-------------|
| exchangeTradeId | Unique trade ID from exchange |
| tradedPrice | Execution price |
| filledQuantity | Executed quantity |
| fillTimestamp | Trade execution time |

[[Back to top]](#) [[Back to README]](../README.md)
