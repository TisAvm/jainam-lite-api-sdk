"""
Browser-based login automation for Jainam Lite API testing.

Uses Selenium + ChromeDriver to automate:
1. Navigate to Jainam SSO login page
2. Enter credentials (user_id, password)
3. Generate and enter TOTP
4. Capture the redirect URL with authCode

NOTE: This is for TESTING purposes only - not part of the public SDK.
"""

import os
import sys
import time
from typing import Tuple
from urllib.parse import urlparse, parse_qs

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pyotp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def get_auth_code_via_browser(
    user_id: str,
    password: str,
    totp_secret: str,
    app_code: str,
    headless: bool = False,
    timeout: int = 60
) -> Tuple[str, str]:
    """
    Automate browser login to get authCode and userId.
    
    Args:
        user_id: Jainam user ID (e.g., RAI03)
        password: Jainam account password
        totp_secret: TOTP secret key for generating OTP
        app_code: Application code for vendor login
        headless: Run browser in headless mode (default: False)
        timeout: Max wait time in seconds (default: 60)
        
    Returns:
        Tuple of (auth_code, user_id) extracted from redirect URL
    """
    # Setup Chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=520,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Initialize driver
    print("Starting Chrome browser...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(timeout)
    
    try:
        # Navigate to SSO login
        login_url = f"https://protrade.jainam.in/?appcode={app_code}"
        print(f"Navigating to: {login_url}")
        driver.get(login_url)
        
        wait = WebDriverWait(driver, timeout)
        
        # Wait for page to fully load
        time.sleep(3)
        
        # Step 1: Enter User ID
        print("Step 1: Entering User ID...")
        try:
            user_input = wait.until(EC.presence_of_element_located((By.ID, "user")))
            user_input.clear()
            user_input.send_keys(user_id)
            print(f"  Entered: {user_id}")
            
            # Click Continue
            continue_btn = wait.until(EC.element_to_be_clickable((By.ID, "user_con_btn")))
            continue_btn.click()
            print("  Clicked Continue")
        except TimeoutException:
            # Try alternate ID
            print("  Trying alternate selector...")
            user_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
            user_input.send_keys(user_id)
            driver.find_element(By.CSS_SELECTOR, "button").click()
        
        time.sleep(2)
        
        # Step 2: Enter Password
        print("Step 2: Entering Password...")
        try:
            password_input = wait.until(EC.presence_of_element_located((By.ID, "passcode")))
            password_input.clear()
            password_input.send_keys(password)
            print("  Entered password")
            
            # Click Continue
            pass_continue_btn = wait.until(EC.element_to_be_clickable((By.ID, "pass_con_btn")))
            pass_continue_btn.click()
            print("  Clicked Continue")
        except TimeoutException:
            print("  Trying alternate selector...")
            password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_input.send_keys(password)
            driver.find_element(By.CSS_SELECTOR, "button").click()
        
        time.sleep(2)
        
        # Step 3: Enter TOTP
        print("Step 3: Entering TOTP...")
        
        # Generate TOTP
        totp = pyotp.TOTP(totp_secret)
        otp_code = totp.now()
        print(f"  Generated TOTP: {otp_code}")
        
        try:
            totp_input = wait.until(EC.presence_of_element_located((By.ID, "totp_input")))
            totp_input.clear()
            totp_input.send_keys(otp_code)
            print("  Entered TOTP")
            
            # Click Continue
            totp_continue_btn = wait.until(EC.element_to_be_clickable((By.ID, "totp_con_btn")))
            totp_continue_btn.click()
            print("  Clicked Continue")
        except TimeoutException:
            print("  Trying alternate selector...")
            totp_input = driver.find_element(By.CSS_SELECTOR, "input[inputmode='numeric']")
            totp_input.send_keys(otp_code)
            driver.find_element(By.CSS_SELECTOR, "button").click()
        
        # Wait for redirect with authCode in URL
        print("Step 4: Waiting for redirect...")
        
        def url_contains_authcode(d):
            return "authCode" in d.current_url
        
        wait.until(url_contains_authcode)
        
        redirect_url = driver.current_url
        print(f"  Redirect URL obtained!")
        
        # Parse authCode and userId from URL
        parsed = urlparse(redirect_url)
        params = parse_qs(parsed.query)
        
        auth_code = params.get('authCode', [''])[0]
        if ',' in auth_code:
            auth_code = auth_code.split(',')[0]
            
        user_id_from_url = params.get('userId', [''])[0]
        if ',' in user_id_from_url:
            user_id_from_url = user_id_from_url.split(',')[0]
        
        print(f"\n[OK] Login successful!")
        print(f"     authCode: {auth_code}")
        print(f"     userId: {user_id_from_url}")
        
        return auth_code, user_id_from_url
        
    except Exception as e:
        print(f"\n[FAIL] Error during login: {e}")
        # Take screenshot for debugging
        try:
            driver.save_screenshot("login_error.png")
            print("  Screenshot saved to login_error.png")
        except:
            pass
        raise
        
    finally:
        driver.quit()
        print("Browser closed.")


def get_auth_code_from_env(headless: bool = False) -> Tuple[str, str]:
    """
    Get authCode using credentials from environment variables.
    
    Reads from:
    - JAINAM_USER_ID
    - JAINAM_USER_PASSWORD
    - TOTP_TOKEN
    - JAINAM_APP_CODE
    
    Returns:
        Tuple of (auth_code, user_id)
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    user_id = os.getenv("JAINAM_USER_ID")
    password = os.getenv("JAINAM_USER_PASSWORD")
    totp_secret = os.getenv("TOTP_TOKEN")
    app_code = os.getenv("JAINAM_APP_CODE")
    
    if not all([user_id, password, totp_secret, app_code]):
        missing = []
        if not user_id: missing.append("JAINAM_USER_ID")
        if not password: missing.append("JAINAM_USER_PASSWORD")
        if not totp_secret: missing.append("TOTP_TOKEN")
        if not app_code: missing.append("JAINAM_APP_CODE")
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return get_auth_code_via_browser(
        user_id=user_id,
        password=password,
        totp_secret=totp_secret,
        app_code=app_code,
        headless=headless
    )


def auto_login_and_cache() -> 'SessionManager':
    """
    Automatically login via browser and cache the session.
    
    Returns:
        SessionManager with valid session
    """
    from jainam_api_client import SessionManager
    
    print("=" * 60)
    print("JAINAM AUTO LOGIN (Selenium)")
    print("=" * 60)
    
    # Get authCode via browser automation
    auth_code, user_id = get_auth_code_from_env(headless=False)
    
    # Login with SessionManager
    print("\nCaching session...")
    sm = SessionManager()
    response = sm.login_with_authcode(auth_code)
    
    if response.get("status") != "Ok":
        raise ValueError(f"Login failed: {response}")
    
    print(f"[OK] Session cached to: {sm.session_file}")
    return sm


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("JAINAM SELENIUM AUTO-LOGIN TEST")
    print("=" * 60 + "\n")
    
    try:
        sm = auto_login_and_cache()
        print("\n[OK] Auto-login successful!")
        print("     You can now run: python tests/run_cached_tests.py")
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
