"""
Test WebSocket APIs

This module tests WebSocket market data subscription functionality.

Functions tested:
- create_websocket_session(): Create WebSocket session
- subscribe(): Subscribe to market data
- unsubscribe(): Unsubscribe from market data

Note: WebSocket tests require a stable connection and may timeout
if the market is closed or connection issues occur.
"""

import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from jainam_api_client import JainamAPI
from tests.test_auth import get_authenticated_api


# Test instruments for subscription
TEST_INSTRUMENTS = [
    {"exchange": "NSE", "token": "26000"},  # NIFTY 50
    {"exchange": "NSE", "token": "26009"},  # NIFTY BANK
]


def test_create_websocket_session(api: JainamAPI):
    """Test WebSocket session creation."""
    print("\n" + "=" * 50)
    print("Testing: create_websocket_session()")
    print("=" * 50)
    
    if api is None:
        print("SKIPPED: No authenticated API instance")
        return None
    
    try:
        response = api.create_websocket_session()
        print(f"SUCCESS: WebSocket session created")
        print(f"  Response: {response}")
        return response
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return None


def test_subscribe(api: JainamAPI):
    """Test market data subscription."""
    print("\n" + "=" * 50)
    print("Testing: subscribe()")
    print("=" * 50)
    
    if api is None:
        print("SKIPPED: No authenticated API instance")
        return None
    
    try:
        # Subscribe to tick data
        response = api.subscribe(
            instruments=TEST_INSTRUMENTS,
            is_depth=False,
        )
        print(f"SUCCESS: Subscribed to tick data")
        print(f"  Instruments: {TEST_INSTRUMENTS}")
        print(f"  Response: {response}")
        
        # Wait a bit to receive some data
        print("\n  Waiting 3 seconds for data...")
        time.sleep(3)
        
        return response
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return None


def test_subscribe_depth(api: JainamAPI):
    """Test depth data subscription."""
    print("\n" + "=" * 50)
    print("Testing: subscribe() - Depth Data")
    print("=" * 50)
    
    if api is None:
        print("SKIPPED: No authenticated API instance")
        return None
    
    try:
        # Subscribe to depth data
        response = api.subscribe(
            instruments=TEST_INSTRUMENTS,
            is_depth=True,
        )
        print(f"SUCCESS: Subscribed to depth data")
        print(f"  Response: {response}")
        
        # Wait a bit to receive some data
        print("\n  Waiting 3 seconds for depth data...")
        time.sleep(3)
        
        return response
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return None


def test_unsubscribe(api: JainamAPI):
    """Test unsubscription."""
    print("\n" + "=" * 50)
    print("Testing: unsubscribe()")
    print("=" * 50)
    
    if api is None:
        print("SKIPPED: No authenticated API instance")
        return None
    
    try:
        # Unsubscribe from tick data
        response = api.unsubscribe(
            instruments=TEST_INSTRUMENTS,
            is_depth=False,
        )
        print(f"SUCCESS: Unsubscribed from tick data")
        print(f"  Response: {response}")
        return response
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return None


def test_unsubscribe_depth(api: JainamAPI):
    """Test depth unsubscription."""
    print("\n" + "=" * 50)
    print("Testing: unsubscribe() - Depth")
    print("=" * 50)
    
    if api is None:
        print("SKIPPED: No authenticated API instance")
        return None
    
    try:
        # Unsubscribe from depth data
        response = api.unsubscribe(
            instruments=TEST_INSTRUMENTS,
            is_depth=True,
        )
        print(f"SUCCESS: Unsubscribed from depth data")
        print(f"  Response: {response}")
        return response
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return None


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# JAINAM LITE API SDK - WebSocket Tests")
    print("#" * 60)
    print("\nNote: WebSocket tests may take longer due to connection setup.")
    print("Market must be open for real-time data.\n")
    
    # Get authenticated API
    api = get_authenticated_api()
    
    if api is None:
        print("ERROR: Could not authenticate. Check your .env file.")
    else:
        # Test create WebSocket session
        test_create_websocket_session(api)
        
        # Test subscribe to tick data
        test_subscribe(api)
        
        # Test subscribe to depth data
        test_subscribe_depth(api)
        
        # Test unsubscribe from tick
        test_unsubscribe(api)
        
        # Test unsubscribe from depth
        test_unsubscribe_depth(api)
        
        # Logout
        api.logout()
    
    print("\n" + "#" * 60)
    print("# WebSocket Tests Complete")
    print("#" * 60)
