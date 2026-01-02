"""
Funds/Limits API for Jainam Lite API

Handles retrieving account funds and limits.
"""

from typing import Dict, Any

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class FundsAPI:
    """
    Funds/Limits API handler.
    
    Retrieves account balance, margin utilization, and collateral information.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize FundsAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def get_limits(self) -> Dict[str, Any]:
        """
        Get account funds and limits.
        
        Returns trading account balance, margin utilization, and collateral.
        
        Returns:
            Response with fund details containing:
            - tradingLimit: Maximum limit available for trading
            - openingCashLimit: Cash available at start of day
            - intradayPayin: Funds from intraday settlements
            - collateralMargin: Margin from pledged securities
            - creditForSell: Proceeds from securities sold
            - adhocMargin: Extra margin added by broker
            - utilizedMargin: Total margin used
            - blockedForPayout: Funds blocked for payout
            - utilizedSpanMargin: SPAN margin for derivatives
            - utilizedExposureMargin: Exposure margin utilized
            
        Example:
            >>> funds.get_limits()
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "tradingLimit": 0,
                    "openingCashLimit": 52926.40,
                    "collateralMargin": 47735.39,
                    "utilizedMargin": 69.95,
                    ...
                }]
            }
        """
        return self.client.get(urls.LIMITS)
