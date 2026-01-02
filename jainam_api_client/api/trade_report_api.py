"""
Trade Report API for Jainam Lite API

Handles retrieving trade book (executed trades).
"""

from typing import Dict, Any

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class TradeReportAPI:
    """
    Trade report (trade book) API handler.
    
    Retrieves all executed trades for the trading session.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize TradeReportAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def get_trade_book(self) -> Dict[str, Any]:
        """
        Get all executed trades (trade book).
        
        Returns only orders that have been executed (filled).
        
        Returns:
            Response with list of trades containing:
            - brokerOrderId, exchangeOrderId, exchangeTradeId
            - tradingSymbol, instrumentId, exchange
            - transactionType, tradedPrice, filledQuantity
            - orderTime, fillTimestamp
            
        Example:
            >>> trade_report.get_trade_book()
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "clientId": "DK2200295",
                    "brokerOrderId": "250526000005634",
                    "exchangeTradeId": "207745115",
                    "tradingSymbol": "IDEA-EQ",
                    "transactionType": "BUY",
                    "tradedPrice": 6.95,
                    "filledQuantity": 1,
                    ...
                }]
            }
        """
        return self.client.get(urls.TRADE_BOOK)
