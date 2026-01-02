"""
Holdings API for Jainam Lite API

Handles retrieving portfolio holdings.
"""

from typing import Dict, Any

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class HoldingsAPI:
    """
    Holdings API handler.
    
    Retrieves long-term equity holdings from DEMAT account.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize HoldingsAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def get_holdings(self, product_type: str = "cnc") -> Dict[str, Any]:
        """
        Get portfolio holdings.
        
        Holdings are long-term investments residing in DEMAT account.
        Changes settle in T+1 days.
        
        Args:
            product_type: Product type filter:
                - "cnc" -> LONGTERM holdings
                - "mtf" -> MTF holdings
                - "mis" -> INTRADAY (usually empty as squared off)
                
        Returns:
            Response with list of holdings containing:
            - isin, nseInstrumentId, bseInstrumentId
            - nseTradingSymbol, bseTradingSymbol
            - formattedInstrumentName
            - product, averageTradedPrice
            - totalQuantity, dpQuantity
            - t1Quantity, collateralQuantity
            
        Example:
            >>> holdings.get_holdings()
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "isin": "INE117A01022",
                    "nseTradingSymbol": "ABB-EQ",
                    "formattedInstrumentName": "ABB",
                    "product": "LONGTERM",
                    "totalQuantity": 10,
                    ...
                }]
            }
        """
        endpoint = urls.HOLDINGS.format(product_type=product_type)
        return self.client.get(endpoint)
