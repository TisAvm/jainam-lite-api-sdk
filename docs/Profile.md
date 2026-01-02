# Profile

Get user profile.

```python
client.profile()
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

profile = client.profile()
result = profile.get("result", {})
print(f"Client: {result.get('clientName')}")
print(f"Exchanges: {result.get('exchanges')}")
```

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": {
        "clientId": "DK2200295",
        "clientName": "SUCHI JAINAM PARIKH",
        "isTotpEnabled": "Y",
        "isPoaProvided": "Y",
        "accountStatus": "Activated",
        "exchanges": ["MCX", "NSE", "NFO", "BSE", "BFO"],
        "products": ["LONGTERM", "INTRADAY"],
        "orderComplexity": ["REGULAR", "AMO", "BO", "CO"]
    }
}
```

[[Back to top]](#) [[Back to README]](../README.md)
