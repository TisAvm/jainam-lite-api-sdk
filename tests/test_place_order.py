"""
Test Place Order - Isolated Order Placement Test

This script:
1. Loads session from ~/.jainam_session.json (checksum included)
2. Places a real order on NFO
3. Checks order status from order book
4. Saves full raw responses to output file

WARNING: This will place REAL orders on your account!
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# Output file
OUTPUT_FILE = Path(__file__).parent / "order_test_output.txt"


class OutputLogger:
    """Logger that writes to both console and file."""
    
    def __init__(self):
        self.lines = []
    
    def log(self, message=""):
        print(message)
        self.lines.append(message)
    
    def save(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.lines))


def load_session(logger):
    """Load session from JSON file."""
    from jainam_api_client import SessionManager
    
    sm = SessionManager()
    
    if not sm.load_session():
        logger.log("[ERROR] No session found. Run auto_login.py or test_all_apis.py first.")
        return None
    
    if not sm.is_session_valid():
        logger.log("[WARNING] Session may be expired. Consider running auto_login.py again.")
    
    logger.log("=" * 70)
    logger.log("SESSION LOADED")
    logger.log("=" * 70)
    logger.log(f"User ID:      {sm.user_id}")
    logger.log(f"Checksum:     {sm.checksum}")
    logger.log(f"Access Token: {sm.access_token[:50]}...")
    logger.log(f"Login Time:   {sm.login_time}")
    logger.log(f"Session File: {sm.session_file}")
    logger.log("=" * 70)
    
    return sm


def place_nfo_order(api, logger):
    """Place order on NFO exchange."""
    
    # Order parameters
    order_params = {
        "exchange": "NFO",
        "instrument_id": "40503",
        "transaction_type": "SELL",
        "quantity": 65,
        "product": "LONGTERM",
        "order_complexity": "REGULAR",
        "order_type": "MARKET",
        "validity": "DAY"
    }
    
    logger.log("")
    logger.log("=" * 70)
    logger.log("STEP 1: PLACING ORDER")
    logger.log("=" * 70)
    logger.log(f"Exchange:         {order_params['exchange']}")
    logger.log(f"Instrument ID:    {order_params['instrument_id']}")
    logger.log(f"Transaction Type: {order_params['transaction_type']}")
    logger.log(f"Quantity:         {order_params['quantity']}")
    logger.log(f"Product:          {order_params['product']}")
    logger.log(f"Order Type:       {order_params['order_type']}")
    logger.log(f"Validity:         {order_params['validity']}")
    logger.log("-" * 70)
    
    try:
        response = api.place_order(
            exchange=order_params["exchange"],
            instrument_id=order_params["instrument_id"],
            transaction_type=order_params["transaction_type"],
            quantity=order_params["quantity"],
            product=order_params["product"],
            order_complexity=order_params["order_complexity"],
            order_type=order_params["order_type"],
            validity=order_params["validity"]
        )
        
        status = response.get("status", "Unknown")
        logger.log(f"Status: {status}")
        logger.log(f"Message: {response.get('message', 'N/A')}")
        
        broker_order_id = None
        if status == "Ok":
            result = response.get("result", [])
            if result:
                order_data = result[0] if isinstance(result, list) else result
                broker_order_id = order_data.get("brokerOrderId", None)
                logger.log(f"Broker Order ID: {broker_order_id}")
                logger.log("[SUCCESS] Order placed!")
            else:
                logger.log("[SUCCESS] Order placed (no order ID in response)")
        else:
            logger.log(f"[FAILED] {response.get('message', response)}")
        
        return response, broker_order_id, order_params
        
    except Exception as e:
        logger.log(f"[ERROR] {type(e).__name__}: {e}")
        return {"error": str(e)}, None, order_params


def check_order_status(api, broker_order_id, logger):
    """Check order status from order book."""
    
    logger.log("")
    logger.log("=" * 70)
    logger.log("STEP 2: CHECK ORDER STATUS")
    logger.log("=" * 70)
    
    if not broker_order_id:
        logger.log("[SKIP] No broker order ID to check")
        return None
    
    logger.log(f"Looking for Order ID: {broker_order_id}")
    logger.log("-" * 70)
    
    # Wait a moment for order to be processed
    logger.log("Waiting 2 seconds for order processing...")
    time.sleep(2)
    
    try:
        # Get order book
        response = api.order_report()
        
        status = response.get("status", "Unknown")
        logger.log(f"Order Book Status: {status}")
        
        if status == "Ok":
            orders = response.get("result", [])
            logger.log(f"Total Orders in Book: {len(orders) if orders else 0}")
            
            # Find our order
            our_order = None
            for order in (orders or []):
                if order.get("brokerOrderId") == broker_order_id:
                    our_order = order
                    break
            
            if our_order:
                logger.log("")
                logger.log(">>> OUR ORDER FOUND <<<")
                logger.log(f"  Order Status:     {our_order.get('orderStatus', 'N/A')}")
                logger.log(f"  Trading Symbol:   {our_order.get('tradingSymbol', 'N/A')}")
                logger.log(f"  Exchange:         {our_order.get('exchange', 'N/A')}")
                logger.log(f"  Transaction Type: {our_order.get('transactionType', 'N/A')}")
                logger.log(f"  Quantity:         {our_order.get('quantity', 'N/A')}")
                logger.log(f"  Filled Qty:       {our_order.get('filledQuantity', 'N/A')}")
                logger.log(f"  Pending Qty:      {our_order.get('pendingQuantity', 'N/A')}")
                logger.log(f"  Price:            {our_order.get('price', 'N/A')}")
                logger.log(f"  Avg Traded Price: {our_order.get('averageTradedPrice', 'N/A')}")
                logger.log(f"  Order Time:       {our_order.get('orderTime', 'N/A')}")
                logger.log(f"  Rejection Reason: {our_order.get('rejectionReason', 'N/A')}")
                return {"order_book": response, "our_order": our_order}
            else:
                logger.log(f"[WARNING] Order {broker_order_id} not found in order book")
        
        return {"order_book": response, "our_order": None}
        
    except Exception as e:
        logger.log(f"[ERROR] {type(e).__name__}: {e}")
        return {"error": str(e)}


def save_raw_responses(sm, order_params, place_response, status_response, logger):
    """Save all raw responses to output."""
    
    logger.log("")
    logger.log("=" * 70)
    logger.log("RAW API RESPONSES")
    logger.log("=" * 70)
    
    logger.log("")
    logger.log(">>> PLACE ORDER RESPONSE <<<")
    logger.log("-" * 40)
    logger.log(json.dumps(place_response, indent=2, default=str))
    
    if status_response:
        logger.log("")
        logger.log(">>> ORDER STATUS (from Order Book) <<<")
        logger.log("-" * 40)
        if status_response.get("our_order"):
            logger.log(json.dumps(status_response["our_order"], indent=2, default=str))
        else:
            logger.log("Order not found in order book")
        
        logger.log("")
        logger.log(">>> FULL ORDER BOOK RESPONSE <<<")
        logger.log("-" * 40)
        if status_response.get("order_book"):
            logger.log(json.dumps(status_response["order_book"], indent=2, default=str))
    
    # Save JSON file
    json_file = Path(__file__).parent / "order_test_results.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": sm.user_id,
            "checksum": sm.checksum,
            "order_params": order_params,
            "place_order_response": place_response,
            "order_status_response": status_response
        }, f, indent=2, default=str)
    
    logger.log("")
    logger.log(f"JSON saved to: {json_file}")


def main():
    logger = OutputLogger()
    
    logger.log("#" * 70)
    logger.log("# NFO ORDER TEST")
    logger.log(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.log("#" * 70)
    logger.log("")
    logger.log("WARNING: This will place a REAL order!")
    logger.log("Exchange: NFO | Instrument: 40503 | SELL | Qty: 65 | MARKET")
    logger.log("")
    
    # Confirm before placing
    
    confirm = input("Type 'YES' to proceed: ")
    if confirm != "YES":
        print("Aborted.")
        return
    
    # Load session
    sm = load_session(logger)
    if not sm:
        logger.save(OUTPUT_FILE)
        return
    
    api = sm.get_api_client()
    
    # Step 1: Place order
    place_response, broker_order_id, order_params = place_nfo_order(api, logger)
    
    # Step 2: Check order status
    status_response = check_order_status(api, broker_order_id, logger)
    
    # Save all raw responses
    save_raw_responses(sm, order_params, place_response, status_response, logger)
    
    logger.log("")
    logger.log("#" * 70)
    logger.log("# ORDER TEST COMPLETE")
    logger.log("#" * 70)
    
    # Save output
    logger.save(OUTPUT_FILE)
    print(f"\nOutput saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
