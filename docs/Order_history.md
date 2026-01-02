# Order History

Get order history/audit trail for a specific order.

```python
client.order_history(broker_order_id="")
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()
client.set_access_token("your_token")

history = client.order_history(broker_order_id="250526000002881")
for state in history.get("result", []):
    print(f"{state['orderStatus']}")
```

## Parameters

| Name | Description | Type |
|------|-------------|------|
| *broker_order_id* | Order ID | Str (required) |

## Response

Shows all state transitions:
- `put order req received`
- `validation pending`
- `open pending`
- `open`
- `complete` / `cancelled` / `rejected`

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [
        {"orderStatus": "open", ...},
        {"orderStatus": "open pending", ...},
        {"orderStatus": "validation pending", ...},
        {"orderStatus": "put order req received", ...}
    ]
}
```

[[Back to top]](#) [[Back to README]](../README.md)
