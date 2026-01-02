# Jainam Lite API SDK - Tests

Integration tests for the Jainam Lite API SDK.

## Setup

### 1. Install SDK in Development Mode

```bash
cd jainam-lite-api-sdk
pip install -e .
```

### 2. Install Test Dependencies

```bash
pip install -r tests/requirements.txt
```

### 3. Configure Credentials

Copy `.env.example` to `.env` in the project root and fill in:

```env
JAINAM_USER_ID=your_user_id
JAINAM_USER_PASSWORD=your_password
TOTP_TOKEN=your_totp_secret
JAINAM_API_SECRET=your_api_secret
JAINAM_APP_CODE=your_app_code
```

## Test Files

| File | Description |
|------|-------------|
| `auto_login.py` | Selenium auto-login - gets authCode automatically |
| `test_all_apis.py` | Unified test - login + test all API endpoints |
| `test_place_order.py` | Isolated order test - places real NFO order |
| `test_websocket.py` | WebSocket streaming tests |

## Running Tests

### Option 1: Unified Test (Recommended)

Runs Selenium auto-login, saves session, then tests all APIs:

```bash
python tests/test_all_apis.py
```

### Option 2: Auto-Login Only

Just performs login and saves session to `~/.jainam_session.json`:

```bash
python tests/auto_login.py
```

### Option 3: Use Cached Session

After running auto_login once, you can use the cached session:

```python
from jainam_api_client import SessionManager

sm = SessionManager()
if sm.load_session() and sm.is_session_valid():
    api = sm.get_api_client()
    print(api.limits())
```

## Session Caching

Sessions are cached to `~/.jainam_session.json` with:
- `access_token` - JWT for API authentication
- `checksum` - SHA-256 hash for verification
- `login_time` - For session expiry validation

## Warning

⚠️ These are **LIVE API** tests. Order tests will place real orders.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AuthCode already used | AuthCodes are one-time. Run auto_login again. |
| Session expired | Sessions expire daily. Run auto_login again. |
| Invalid JSON response | Clear session: `SessionManager().clear_session()` |