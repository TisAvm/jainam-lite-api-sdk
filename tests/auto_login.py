"""
Simple Selenium auto-login for Jainam API.
"""

import os
import sys
import time
from urllib.parse import urlparse, parse_qs

# Add project root to path (parent of tests folder)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import pyotp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    # Get env vars
    user_id = os.getenv("JAINAM_USER_ID")
    password = os.getenv("JAINAM_USER_PASSWORD")
    totp_secret = os.getenv("TOTP_TOKEN")
    app_code = os.getenv("JAINAM_APP_CODE")
    
    print("=" * 50)
    print("JAINAM SELENIUM AUTO-LOGIN")
    print("=" * 50)
    print(f"User ID: {user_id}")
    print(f"App Code: {app_code}")
    
    # Start Chrome
    print("\nStarting Chrome...")
    driver = webdriver.Chrome()
    
    try:
        # Navigate
        url = f"https://protrade.jainam.in/?appcode={app_code}"
        print(f"Opening: {url}")
        driver.get(url)
        
        wait = WebDriverWait(driver, 30)
        time.sleep(3)
        
        # Step 1: User ID
        print("\n[1] Entering User ID...")
        user_input = wait.until(EC.presence_of_element_located((By.ID, "user")))
        user_input.send_keys(user_id)
        driver.find_element(By.ID, "user_con_btn").click()
        time.sleep(2)
        
        # Step 2: Password
        print("[2] Entering Password...")
        pass_input = wait.until(EC.presence_of_element_located((By.ID, "passcode")))
        pass_input.send_keys(password)
        driver.find_element(By.ID, "pass_con_btn").click()
        time.sleep(2)
        
        # Step 3: TOTP
        print("[3] Entering TOTP...")
        totp = pyotp.TOTP(totp_secret)
        otp = totp.now()
        # Calculate time until next TOTP changes
        import datetime
        remaining = 30 - (datetime.datetime.now().second % 30)
        print(f"    Generated: {otp} (valid for {remaining}s)")
        
        # Wait a moment if TOTP is about to expire
        if remaining < 5:
            print(f"    TOTP about to expire, waiting {remaining + 2}s for new code...")
            time.sleep(remaining + 2)
            otp = totp.now()
            print(f"    New TOTP: {otp}")
        
        totp_input = wait.until(EC.presence_of_element_located((By.ID, "totp_input")))
        totp_input.send_keys(otp)
        driver.find_element(By.ID, "totp_con_btn").click()
        time.sleep(3)  # Wait for response
        
        # Check for any errors or invalid TOTP message
        try:
            page_source = driver.page_source.lower()
            if "invalid" in page_source or "incorrect" in page_source or "error" in page_source:
                print("    [WARNING] Possible error on page after TOTP submission")
                # Try to find any visible error text
                for msg_class in ['error-message', 'error', 'alert', 'toast']:
                    try:
                        elems = driver.find_elements(By.CLASS_NAME, msg_class)
                        for elem in elems:
                            if elem.is_displayed() and elem.text:
                                print(f"    [ERROR] Found message: {elem.text}")
                    except:
                        pass
        except:
            pass
        
        # Wait for redirect with polling and debugging
        print("[4] Waiting for redirect...")
        max_wait = 60  # seconds
        start_time = time.time()
        auth_code = None
        
        while time.time() - start_time < max_wait:
            current_url = driver.current_url
            print(f"    Current URL: {current_url[:80]}...")
            
            if "authCode" in current_url:
                parsed = urlparse(current_url)
                params = parse_qs(parsed.query)
                auth_code = params.get('authCode', [''])[0].split(',')[0]
                break
            
            # Check for error messages on page
            try:
                error_elem = driver.find_element(By.CLASS_NAME, "error-message")
                if error_elem.text:
                    print(f"    [ERROR] Page error: {error_elem.text}")
                    break
            except:
                pass
            
            time.sleep(2)
        
        if not auth_code:
            print(f"[FAIL] Timeout waiting for redirect. Final URL: {driver.current_url}")
            return
        
        print(f"\n[OK] Got authCode: {auth_code}")
        
        # Cache session
        from jainam_api_client import SessionManager
        sm = SessionManager()
        response = sm.login_with_authcode(auth_code)
        print(f"API Login Response: {response}")
        
        if response.get("status") == "Ok":
            print(f"[OK] Session cached to: {sm.session_file}")
        else:
            print(f"[FAIL] {response}")
            
    finally:
        driver.quit()
        print("\nBrowser closed.")


if __name__ == "__main__":
    main()
