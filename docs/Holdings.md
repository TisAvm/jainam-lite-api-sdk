# Holdings

Get portfolio holdings.

```python
client.holdings(product_type="cnc")
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

holdings = client.holdings()
for holding in holdings.get("result", []):
    print(f"{holding['formattedInstrumentName']}: {holding['totalQuantity']} shares")
```

## Parameters

| Name | Description | Type |
|------|-------------|------|
| *product_type* | cnc (LONGTERM), mtf, mis (INTRADAY) | Str (default: cnc) |

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "isin": "INE117A01022",
        "nseInstrumentId": "13",
        "bseInstrumentId": "500002",
        "nseTradingSymbol": "ABB-EQ",
        "bseTradingSymbol": "ABB",
        "previousDayClose": 0.0,
        "product": "LONGTERM",
        "formattedInstrumentName": "ABB",
        "averageTradedPrice": 0,
        "collateralQuantity": 0,
        "authorizedQuantity": 0,
        "dpQuantity": 0,
        "totalQuantity": 0,
        "t1Quantity": 0
    }]
}
```

[[Back to top]](#) [[Back to README]](../README.md)
