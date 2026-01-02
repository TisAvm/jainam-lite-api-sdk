"""
Unified API Test - Login and Test All Endpoints

This script:
1. Performs auto-login via Selenium (gets fresh authCode)
2. Creates checksum and exchanges for session token
3. Saves session to JSON file
4. Tests all API endpoints using the saved session
5. Outputs detailed results to test_output.txt
"""

import os
import sys
import time
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# Output file
OUTPUT_FILE = Path(__file__).parent / "test_output.txt"


class OutputLogger:
    """Logger that writes to both console and file."""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = []
    
    def log(self, message=""):
        print(message)
        self.lines.append(message)
    
    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.lines))


def selenium_login(logger):
    """Perform Selenium auto-login and get authCode."""
    import pyotp
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    user_id = os.getenv("JAINAM_USER_ID")
    password = os.getenv("JAINAM_USER_PASSWORD")
    totp_secret = os.getenv("TOTP_TOKEN")
    app_code = os.getenv("JAINAM_APP_CODE")
    
    logger.log("=" * 70)
    logger.log("STEP 1: SELENIUM AUTO-LOGIN")
    logger.log("=" * 70)
    logger.log(f"User ID: {user_id}")
    logger.log(f"App Code: {app_code}")
    
    driver = webdriver.Chrome()
    auth_code = None
    
    try:
        url = f"https://protrade.jainam.in/?appcode={app_code}"
        logger.log(f"Opening: {url}")
        driver.get(url)
        
        wait = WebDriverWait(driver, 30)
        time.sleep(3)
        
        # Step 1: User ID
        logger.log("[1] Entering User ID...")
        user_input = wait.until(EC.presence_of_element_located((By.ID, "user")))
        user_input.send_keys(user_id)
        driver.find_element(By.ID, "user_con_btn").click()
        time.sleep(2)
        
        # Step 2: Password
        logger.log("[2] Entering Password...")
        pass_input = wait.until(EC.presence_of_element_located((By.ID, "passcode")))
        pass_input.send_keys(password)
        driver.find_element(By.ID, "pass_con_btn").click()
        time.sleep(2)
        
        # Step 3: TOTP
        logger.log("[3] Entering TOTP...")
        totp = pyotp.TOTP(totp_secret)
        otp = totp.now()
        remaining = 30 - (datetime.now().second % 30)
        logger.log(f"    Generated OTP: {otp} (valid for {remaining}s)")
        
        if remaining < 5:
            logger.log(f"    TOTP about to expire, waiting {remaining + 2}s...")
            time.sleep(remaining + 2)
            otp = totp.now()
        
        totp_input = wait.until(EC.presence_of_element_located((By.ID, "totp_input")))
        totp_input.send_keys(otp)
        driver.find_element(By.ID, "totp_con_btn").click()
        time.sleep(3)
        
        # Wait for redirect
        logger.log("[4] Waiting for redirect...")
        max_wait = 60
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            current_url = driver.current_url
            if "authCode" in current_url:
                parsed = urlparse(current_url)
                params = parse_qs(parsed.query)
                auth_code = params.get('authCode', [''])[0].split(',')[0]
                break
            time.sleep(2)
        
        if auth_code:
            logger.log(f"[OK] Got authCode: {auth_code}")
        else:
            logger.log("[FAIL] Timeout waiting for redirect")
            
    finally:
        driver.quit()
        logger.log("Browser closed.")
    
    return auth_code


def exchange_for_session(auth_code, logger):
    """Exchange authCode for session token and save to JSON."""
    from jainam_api_client import SessionManager
    
    logger.log("")
    logger.log("=" * 70)
    logger.log("STEP 2: EXCHANGE AUTHCODE FOR SESSION")
    logger.log("=" * 70)
    
    sm = SessionManager()
    response = sm.login_with_authcode(auth_code)
    
    logger.log(f"API Response Status: {response.get('status')}")
    logger.log(f"API Response Message: {response.get('message')}")
    
    if response.get("status") == "Ok":
        logger.log("")
        logger.log("SESSION DETAILS:")
        logger.log("-" * 40)
        logger.log(f"  User ID:      {sm.user_id}")
        logger.log(f"  App Code:     {sm.app_code}")
        logger.log(f"  Checksum:     {sm.checksum}")
        logger.log(f"  Access Token: {sm.access_token[:50]}...")
        logger.log(f"  Login Time:   {sm.login_time}")
        logger.log(f"  Session File: {sm.session_file}")
        logger.log("-" * 40)
        return sm, response
    else:
        logger.log(f"[FAIL] {response.get('message', response)}")
        return None, response


def test_all_apis(sm, logger):
    """Test all API endpoints using the saved session."""
    
    logger.log("")
    logger.log("=" * 70)
    logger.log("STEP 3: TEST ALL API ENDPOINTS")
    logger.log("=" * 70)
    
    api = sm.get_api_client()
    results = {}
    responses = {}
    
    # Test 1: Funds/Limits
    logger.log("")
    logger.log("[Test 1] Funds/Limits")
    logger.log("-" * 40)
    try:
        response = api.limits()
        responses["limits"] = response
        status = response.get("status", "Unknown")
        results["limits"] = status
        logger.log(f"  Status: {status}")
        logger.log(f"  Message: {response.get('message', 'N/A')}")
        if status == "Ok":
            result = response.get("result", [])
            if result:
                data = result[0] if isinstance(result, list) else result
                logger.log(f"  Trading Limit: {data.get('tradingLimit', 'N/A')}")
                logger.log(f"  Opening Cash: {data.get('openingCashLimit', 'N/A')}")
                logger.log(f"  Collateral: {data.get('collateralMargin', 'N/A')}")
    except Exception as e:
        results["limits"] = f"Error: {e}"
        logger.log(f"  Error: {e}")
    
    # Test 2: Order Book
    logger.log("")
    logger.log("[Test 2] Order Book")
    logger.log("-" * 40)
    try:
        response = api.order_report()
        responses["order_book"] = response
        status = response.get("status", "Unknown")
        results["order_book"] = status
        logger.log(f"  Status: {status}")
        logger.log(f"  Message: {response.get('message', 'N/A')}")
        if status == "Ok":
            orders = response.get("result", [])
            logger.log(f"  Orders count: {len(orders) if orders else 0}")
            if orders and len(orders) > 0:
                order = orders[0]
                logger.log(f"  Last Order: {order.get('tradingSymbol')} - {order.get('orderStatus')}")
    except Exception as e:
        results["order_book"] = f"Error: {e}"
        logger.log(f"  Error: {e}")
    
    # Test 3: Positions
    logger.log("")
    logger.log("[Test 3] Positions")
    logger.log("-" * 40)
    try:
        response = api.positions()
        responses["positions"] = response
        status = response.get("status", "Unknown")
        results["positions"] = status
        logger.log(f"  Status: {status}")
        logger.log(f"  Message: {response.get('message', 'N/A')}")
        if status == "Ok":
            positions = response.get("result", [])
            logger.log(f"  Positions count: {len(positions) if positions else 0}")
    except Exception as e:
        results["positions"] = f"Error: {e}"
        logger.log(f"  Error: {e}")
    
    # Test 4: Holdings
    logger.log("")
    logger.log("[Test 4] Holdings")
    logger.log("-" * 40)
    try:
        response = api.holdings()
        responses["holdings"] = response
        status = response.get("status", "Unknown")
        results["holdings"] = status
        logger.log(f"  Status: {status}")
        logger.log(f"  Message: {response.get('message', 'N/A')}")
        if status == "Ok":
            holdings = response.get("result", [])
            logger.log(f"  Holdings count: {len(holdings) if holdings else 0}")
    except Exception as e:
        results["holdings"] = f"Error: {e}"
        logger.log(f"  Error: {e}")
    
    # Test 5: Profile
    logger.log("")
    logger.log("[Test 5] Profile")
    logger.log("-" * 40)
    try:
        response = api.profile()
        responses["profile"] = response
        status = response.get("status", "Unknown")
        results["profile"] = status
        logger.log(f"  Status: {status}")
        logger.log(f"  Message: {response.get('message', 'N/A')}")
        if status == "Ok":
            result = response.get("result", {})
            if result:
                data = result[0] if isinstance(result, list) else result
                logger.log(f"  Name: {data.get('name', data.get('userName', 'N/A'))}")
                logger.log(f"  Client ID: {data.get('clientId', 'N/A')}")
                logger.log(f"  Email: {data.get('email', 'N/A')}")
    except Exception as e:
        results["profile"] = f"Error: {e}"
        logger.log(f"  Error: {e}")
    
    # Test 6: Trade Book
    logger.log("")
    logger.log("[Test 6] Trade Book")
    logger.log("-" * 40)
    try:
        response = api.trade_report()
        responses["trade_book"] = response
        status = response.get("status", "Unknown")
        results["trade_book"] = status
        logger.log(f"  Status: {status}")
        logger.log(f"  Message: {response.get('message', 'N/A')}")
        if status == "Ok":
            trades = response.get("result", [])
            logger.log(f"  Trades count: {len(trades) if trades else 0}")
    except Exception as e:
        results["trade_book"] = f"Error: {e}"
        logger.log(f"  Error: {e}")
    
    return results, responses


def print_summary(results, responses, sm, logger):
    """Print test summary."""
    logger.log("")
    logger.log("=" * 70)
    logger.log("TEST SUMMARY")
    logger.log("=" * 70)
    
    passed = 0
    failed = 0
    
    for test, status in results.items():
        if status == "Ok":
            logger.log(f"  [PASS] {test}")
            passed += 1
        else:
            logger.log(f"  [FAIL] {test}: {status}")
            failed += 1
    
    logger.log("-" * 70)
    logger.log(f"Total: {passed} passed, {failed} failed")
    logger.log("")
    logger.log("SESSION INFO:")
    logger.log(f"  Checksum: {sm.checksum}")
    logger.log(f"  Session File: {sm.session_file}")
    
    # Print raw responses
    logger.log("")
    logger.log("=" * 70)
    logger.log("RAW API RESPONSES")
    logger.log("=" * 70)
    
    for api_name, response in responses.items():
        logger.log("")
        logger.log(f">>> {api_name.upper()} <<<")
        logger.log("-" * 40)
        logger.log(json.dumps(response, indent=2, default=str))
    
    # Save results to JSON
    results_file = Path(__file__).parent / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": sm.user_id,
            "checksum": sm.checksum,
            "results": results,
            "passed": passed,
            "failed": failed,
            "raw_responses": responses
        }, f, indent=2, default=str)
    logger.log("")
    logger.log(f"Results JSON: {results_file}")


def main():
    logger = OutputLogger(OUTPUT_FILE)
    
    logger.log("#" * 70)
    logger.log("# JAINAM LITE API SDK - UNIFIED TEST")
    logger.log(f"# Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.log("#" * 70)
    
    # Step 1: Selenium login
    auth_code = selenium_login(logger)
    if not auth_code:
        logger.log("[FAIL] Could not get authCode from login")
        logger.save()
        return
    
    # Step 2: Exchange for session
    sm, login_response = exchange_for_session(auth_code, logger)
    if not sm:
        logger.log("[FAIL] Could not get session token")
        logger.save()
        return
    
    # Step 3: Test all APIs
    results, responses = test_all_apis(sm, logger)
    
    # Print summary
    print_summary(results, responses, sm, logger)
    
    logger.log("")
    logger.log("#" * 70)
    logger.log("# TEST COMPLETE")
    logger.log("#" * 70)
    
    # Save output to file
    logger.save()
    print(f"\nOutput saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
