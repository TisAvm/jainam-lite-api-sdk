# Session Init - SSO Authentication

Authenticate using the SSO vendor flow.

## Login Flow

1. Redirect user to: `https://protrade.jainam.in/?appcode={appCode}`
2. User logs in with Jainam credentials
3. User is redirected to your callback URL with `authCode` and `userId`
4. Use SDK to exchange for session token

## Example

```python
from jainam_api_client import JainamAPI

# Initialize client
client = JainamAPI()

# After receiving callback with authCode and userId
response = client.login_with_sso(
    user_id="DK2200295",         # From callback
    auth_code="abc123xyz",       # From callback
    api_secret="your_secret",    # From developer portal
    app_code="your_app_code"     # From developer portal
)

# Session is now active, you can make API calls
profile = client.profile()
```

## Alternative: Direct Token

If you already have a valid JWT token:

```python
client = JainamAPI(access_token="your_jwt_token")
# Or
client.set_access_token("your_jwt_token")
```

## Response

```json
{
    "status": "Ok",
    "message": "Success",
    "result": [{
        "userSession": "eyJhbGciOiJSUzI1NiIsInR5cCI..."
    }]
}
```

## Checksum Generation

The SDK automatically generates the required checksum:
```
checksum = SHA256(userId + authCode + apiSecret)
```

[[Back to top]](#) [[Back to README]](../README.md)
