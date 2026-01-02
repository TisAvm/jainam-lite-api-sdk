"""
Profile API for Jainam Lite API

Handles retrieving user profile information.
"""

from typing import Dict, Any

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class ProfileAPI:
    """
    Profile API handler.
    
    Retrieves user/client profile information.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize ProfileAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def get_profile(self) -> Dict[str, Any]:
        """
        Get user profile information.
        
        Returns client details and account configuration.
        Note: This does not return authentication tokens.
        
        Returns:
            Response with profile containing:
            - clientId: Unique client identifier
            - clientName: Full name of account holder
            - isTotpEnabled: TOTP enabled status (Y/N)
            - isPoaProvided: POA document status (Y/N)
            - accountStatus: Account status (e.g., "Activated")
            - exchanges: List of enabled exchanges
            - products: List of enabled products
            - orderComplexity: List of enabled order types
            
        Example:
            >>> profile.get_profile()
            {
                "status": "Ok",
                "message": "Success",
                "result": {
                    "clientId": "DK2200295",
                    "clientName": "SUCHI JAINAM PARIKH",
                    "isTotpEnabled": "Y",
                    "accountStatus": "Activated",
                    "exchanges": ["MCX", "NSE", "NFO", "BSE", "BFO"],
                    "products": ["LONGTERM", "INTRADAY"],
                    "orderComplexity": ["REGULAR", "AMO", "BO", "CO"]
                }
            }
        """
        return self.client.get(urls.PROFILE)
