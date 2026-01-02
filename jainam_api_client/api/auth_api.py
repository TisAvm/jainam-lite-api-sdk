"""
Authentication API for Jainam Lite API

Handles SSO vendor authentication flow.
"""

import hashlib
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class AuthAPI:
    """
    Authentication API handler.
    
    Supports SSO vendor authentication flow where:
    1. User is redirected to Jainam login
    2. Vendor receives authCode and userId
    3. Vendor creates checksum = SHA256(userId + authCode + apiSecret)
    4. Vendor exchanges checksum for userSession
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize AuthAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def create_checksum(self, user_id: str, auth_code: str, api_secret: str) -> str:
        """
        Create SHA-256 checksum for SSO authentication.
        
        Args:
            user_id: User ID from redirect
            auth_code: Authorization code from redirect
            api_secret: Your API secret from Jainam developer portal
            
        Returns:
            SHA-256 hex digest of concatenated values
        """
        data = f"{user_id}{auth_code}{api_secret}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def parse_redirect_url(url: str) -> Dict[str, str]:
        """
        Parse authCode and userId from SSO redirect URL.
        
        After user logs in at Jainam, they are redirected to your callback URL
        with authCode and userId as query parameters. Use this method to extract them.
        
        Args:
            url: The full redirect URL received after login
                 e.g. "https://your-app.com/callback?authCode=ABC123&userId=DK2200295"
            
        Returns:
            Dictionary with 'auth_code' and 'user_id' keys
            
        Example:
            >>> url = "https://myapp.com?authCode=VBF4V37IN3ON8XMX5IKW&userId=AVM04"
            >>> result = AuthAPI.parse_redirect_url(url)
            >>> print(result)
            {'auth_code': 'VBF4V37IN3ON8XMX5IKW', 'user_id': 'AVM04'}
        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Handle both single and comma-separated values (take first)
        auth_code = params.get('authCode', [''])[0]
        if ',' in auth_code:
            auth_code = auth_code.split(',')[0]
            
        user_id = params.get('userId', [''])[0]
        if ',' in user_id:
            user_id = user_id.split(',')[0]
        
        return {
            'auth_code': auth_code,
            'user_id': user_id
        }
    
    def get_user_session(
        self,
        user_id: str,
        auth_code: str,
        api_secret: str,
        app_code: str
    ) -> Dict[str, Any]:
        """
        Exchange SSO credentials for user session.
        
        This is the main authentication method for vendor flow.
        
        Args:
            user_id: User ID from redirect callback
            auth_code: Authorization code from redirect callback  
            api_secret: Your API secret from developer portal
            app_code: Your App Code from developer portal
            
        Returns:
            Response containing userSession token
            
        Example:
            >>> auth = AuthAPI(client)
            >>> response = auth.get_user_session(
            ...     user_id="DK2200295",
            ...     auth_code="abc123",
            ...     api_secret="your_secret",
            ...     app_code="your_app_code"
            ... )
            >>> session_token = response["result"]["userSession"]
        """
        checksum = self.create_checksum(user_id, auth_code, api_secret)
        
        payload = {
            "userId": user_id,
            "authCode": auth_code,
            "appCode": app_code,
            "checkSum": checksum,
        }
        
        return self.client.post(urls.SSO_VENDOR_DETAILS, payload)
    
    def set_access_token(self, token: str):
        """
        Set access token directly for authentication.
        
        Use this if you already have a valid JWT token.
        
        Args:
            token: JWT access token
        """
        self.client.set_access_token(token)
    
    def create_websocket_session(self, user_id: str, token: str) -> Dict[str, Any]:
        """
        Create WebSocket session for market data.
        
        Args:
            user_id: User ID
            token: Access token
            
        Returns:
            Response with session status
        """
        payload = {
            "source": "API",
            "userId": user_id,
            "token": token,
        }
        return self.client.post(urls.CREATE_WS_SESSION, payload)
    
    def invalidate_websocket_session(self, user_id: str, token: str) -> Dict[str, Any]:
        """
        Invalidate/terminate WebSocket session.
        
        Args:
            user_id: User ID
            token: Access token
            
        Returns:
            Response with invalidation status
        """
        payload = {
            "source": "API",
            "userId": user_id,
            "token": token,
        }
        return self.client.post(urls.INVALIDATE_WS_SESSION, payload)
