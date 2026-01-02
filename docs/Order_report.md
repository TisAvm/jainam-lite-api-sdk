# Order Report

Get order book (all orders).

```python
client.order_report()
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

orders = client.order_report()
for order in orders.get("result", []):
    print(f"{order['brokerOrderId']}: {order['orderStatus']}")
```

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "clientId": "DK2200295",
        "placedBy": "DK2200295",
        "brokerOrderId": "250526000002881",
        "exchange": "NSE",
        "exchangeOrderId": "1100000048194096",
        "formattedInstrumentName": "IDEA",
        "tradingSymbol": "IDEA-EQ",
        "instrumentId": "14366",
        "transactionType": "BUY",
        "quantity": 10,
        "product": "LONGTERM",
        "orderComplexity": "REGULAR",
        "orderType": "LIMIT",
        "price": 6.30,
        "averageTradedPrice": 0.00,
        "slTriggerPrice": 0.00,
        "validity": "DAY",
        "disclosedQuantity": 0,
        "orderTime": "2025-05-26 12:32:05",
        "exchangeUpdateTime": "2025-05-26 12:32:05",
        "rejectionReason": "--",
        "cancelledQuantity": 0,
        "pendingQuantity": 10,
        "filledQuantity": 0,
        "source": "API",
        "orderStatus": "OPEN"
    }]
}
```

## Response Fields

| Field | Description |
|-------|-------------|
| brokerOrderId | Unique order ID |
| exchangeOrderId | Exchange order ID |
| tradingSymbol | Trading symbol |
| transactionType | BUY or SELL |
| quantity | Total quantity |
| price | Order price |
| orderStatus | OPEN, COMPLETE, REJECTED, CANCELLED |
| filledQuantity | Executed quantity |
| pendingQuantity | Pending quantity |

[[Back to top]](#) [[Back to README]](../README.md)
