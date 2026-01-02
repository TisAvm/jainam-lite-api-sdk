"""
REST Client for Jainam Lite API

Handles HTTP requests with JWT token authentication.
"""

import requests
from typing import Optional, Dict, Any

from jainam_api_client.urls import BASE_URL
from jainam_api_client.exceptions import (
    JainamApiException,
    JainamNetworkError,
    JainamAuthError,
    raise_from_response,
)


class RestClient:
    """
    HTTP client for making authenticated requests to Jainam API.
    
    Handles:
    - JWT token management
    - Request/response handling
    - Error handling
    """
    
    def __init__(self, base_url: str = BASE_URL):
        """
        Initialize REST client.
        
        Args:
            base_url: Base URL for API requests
        """
        self.base_url = base_url.rstrip("/")
        self.access_token: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
    
    def set_access_token(self, token: str):
        """
        Set the access token for authentication.
        
        Args:
            token: JWT access token
        """
        self.access_token = token
        # Bearer prefix is required for Jainam API
        self.session.headers["Authorization"] = f"Bearer {token}"
    
    def clear_token(self):
        """Clear the access token."""
        self.access_token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
    
    def _get_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return f"{self.base_url}/{endpoint.lstrip('/')}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response.
        
        Args:
            response: Response object
            
        Returns:
            Parsed JSON response
            
        Raises:
            JainamApiException: If response indicates an error
        """
        try:
            data = response.json()
        except ValueError:
            print(f"DEBUG: Invalid JSON response from {response.url}")
            print(f"DEBUG: Status Code: {response.status_code}")
            print(f"DEBUG: Content: {response.text[:500]}")
            raise JainamApiException(
                f"Invalid JSON response: {response.text}",
                response={"raw": response.text}
            )
        
        # Check for error status
        if response.status_code >= 400:
            if response.status_code == 401:
                raise JainamAuthError(
                    "Unauthorized. Please check your access token.",
                    error_code="EC087",
                    response=data
                )
            raise_from_response(data)
        
        # Check response status field
        if data.get("status") != "Ok":
            raise_from_response(data)
        
        return data
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make GET request.
        
        Args:
            endpoint: API endpoint
            params: Optional query parameters
            
        Returns:
            API response data
        """
        try:
            response = self.session.get(
                self._get_url(endpoint),
                params=params
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            raise JainamNetworkError(f"Network error: {str(e)}")
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make POST request.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            
        Returns:
            API response data
        """
        try:
            response = self.session.post(
                self._get_url(endpoint),
                json=data
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            raise JainamNetworkError(f"Network error: {str(e)}")
    
    def download(self, url: str) -> bytes:
        """
        Download file from URL.
        
        Args:
            url: Full URL to download
            
        Returns:
            File content as bytes
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise JainamNetworkError(f"Download error: {str(e)}")
