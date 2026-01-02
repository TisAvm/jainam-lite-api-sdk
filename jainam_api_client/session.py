"""
Session Manager for Jainam Lite API

Handles:
- AuthCode input and checksum creation
- Session caching in JSON file
- Session loading and validation
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path


# Default session file location
DEFAULT_SESSION_FILE = Path.home() / ".jainam_session.json"


class SessionManager:
    """
    Manages Jainam API session with JSON file caching.
    
    The session flow:
    1. User logs in via browser and gets authCode from redirect URL
    2. Call login_with_authcode() with the authCode
    3. Session (accessToken) is saved to JSON file
    4. Subsequent calls can use load_session() to reuse the token
    
    Example:
        >>> from jainam_api_client.session import SessionManager
        >>> 
        >>> # First time login
        >>> sm = SessionManager()
        >>> sm.login_with_authcode("YOUR_AUTH_CODE")
        >>> 
        >>> # Later - load cached session
        >>> sm = SessionManager()
        >>> if sm.load_session():
        ...     print("Session loaded from cache")
        ... else:
        ...     authcode = input("Enter authCode from redirect: ")
        ...     sm.login_with_authcode(authcode)
    """
    
    def __init__(
        self,
        user_id: Optional[str] = None,
        api_secret: Optional[str] = None,
        app_code: Optional[str] = None,
        session_file: Optional[Path] = None
    ):
        """
        Initialize SessionManager.
        
        Args:
            user_id: Jainam user ID (or from env JAINAM_USER_ID)
            api_secret: API secret (or from env JAINAM_API_SECRET)
            app_code: App code (or from env JAINAM_APP_CODE)
            session_file: Path to session JSON file
        """
        self.user_id = user_id or os.getenv("JAINAM_USER_ID")
        self.api_secret = api_secret or os.getenv("JAINAM_API_SECRET")
        self.app_code = app_code or os.getenv("JAINAM_APP_CODE")
        self.session_file = session_file or DEFAULT_SESSION_FILE
        
        # Session data
        self.access_token: Optional[str] = None
        self.checksum: Optional[str] = None
        self.login_time: Optional[datetime] = None
    
    def create_checksum(self, auth_code: str) -> str:
        """
        Create SHA-256 checksum as per Jainam documentation.
        
        checkSum = SHA-256(userId + authCode + apiSecret)
        
        Args:
            auth_code: Authorization code from redirect URL
            
        Returns:
            SHA-256 hex digest
        """
        data = f"{self.user_id}{auth_code}{self.api_secret}"
        checksum = hashlib.sha256(data.encode()).hexdigest()
        self.checksum = checksum
        return checksum
    
    def login_with_authcode(self, auth_code: str) -> Dict[str, Any]:
        """
        Login using authCode and cache the session.
        
        Args:
            auth_code: Authorization code from browser redirect
            
        Returns:
            API response with accessToken
        """
        from jainam_api_client import JainamAPI
        
        if not all([self.user_id, self.api_secret, self.app_code]):
            raise ValueError(
                "Missing credentials. Set JAINAM_USER_ID, JAINAM_API_SECRET, "
                "JAINAM_APP_CODE in environment or pass to constructor."
            )
        
        # Create checksum
        self.create_checksum(auth_code)
        
        # Login via SDK
        api = JainamAPI()
        response = api.login_with_sso(
            user_id=self.user_id,
            auth_code=auth_code,
            api_secret=self.api_secret,
            app_code=self.app_code
        )
        
        # Extract and cache session
        if response.get("status") == "Ok":
            result = response.get("result", {})
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
            
            self.access_token = result.get("accessToken")
            self.login_time = datetime.now()
            
            # Save to file
            self.save_session()
        
        return response
    
    def save_session(self) -> bool:
        """
        Save current session to JSON file.
        
        Returns:
            True if saved successfully
        """
        if not self.access_token:
            return False
        
        session_data = {
            "user_id": self.user_id,
            "access_token": self.access_token,
            "checksum": self.checksum,
            "login_time": self.login_time.isoformat() if self.login_time else None,
            "app_code": self.app_code,
        }
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Warning: Could not save session: {e}")
            return False
    
    def load_session(self) -> bool:
        """
        Load session from JSON file.
        
        Returns:
            True if session loaded and appears valid
        """
        if not self.session_file.exists():
            return False
        
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)
            
            self.user_id = data.get("user_id")
            self.access_token = data.get("access_token")
            self.checksum = data.get("checksum")
            self.app_code = data.get("app_code")
            
            login_time_str = data.get("login_time")
            if login_time_str:
                self.login_time = datetime.fromisoformat(login_time_str)
            
            return bool(self.access_token)
            
        except Exception as e:
            print(f"Warning: Could not load session: {e}")
            return False
    
    def is_session_valid(self, max_age_hours: int = 8) -> bool:
        """
        Check if cached session is still valid.
        
        Sessions typically expire at end of trading day.
        
        Args:
            max_age_hours: Maximum age in hours (default: 8)
            
        Returns:
            True if session appears valid
        """
        if not self.access_token or not self.login_time:
            return False
        
        age = datetime.now() - self.login_time
        return age < timedelta(hours=max_age_hours)
    
    def clear_session(self):
        """Clear cached session and delete file."""
        self.access_token = None
        self.checksum = None
        self.login_time = None
        
        if self.session_file.exists():
            try:
                os.remove(self.session_file)
            except Exception:
                pass
    
    def get_api_client(self) -> 'JainamAPI':
        """
        Get authenticated JainamAPI client.
        
        Returns:
            Authenticated JainamAPI instance
            
        Raises:
            ValueError: If no valid session
        """
        from jainam_api_client import JainamAPI
        
        if not self.access_token:
            raise ValueError("No session. Call login_with_authcode() or load_session() first.")
        
        api = JainamAPI()
        api.set_access_token(self.access_token)
        api._user_id = self.user_id
        api._session_id = self.access_token
        return api


def interactive_login(session_file: Optional[Path] = None) -> SessionManager:
    """
    Interactive login helper - prompts for authCode if needed.
    
    Returns:
        SessionManager with valid session
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    sm = SessionManager(session_file=session_file)
    
    # Try loading cached session
    if sm.load_session() and sm.is_session_valid():
        print(f"Loaded cached session for user: {sm.user_id}")
        return sm
    
    # Need fresh login
    print("\n" + "=" * 50)
    print("JAINAM LOGIN")
    print("=" * 50)
    print(f"\n1. Open browser: https://protrade.jainam.in/?appcode={sm.app_code}")
    print("2. Login with your Jainam credentials + TOTP")
    print("3. Copy the 'authCode' from the redirect URL")
    print("\n")
    
    auth_code = input("Enter authCode: ").strip()
    
    if not auth_code:
        raise ValueError("authCode is required")
    
    response = sm.login_with_authcode(auth_code)
    
    if response.get("status") == "Ok":
        print(f"\n[OK] Login successful! Session cached to: {sm.session_file}")
    else:
        print(f"\n[FAIL] Login failed: {response}")
        raise ValueError("Login failed")
    
    return sm