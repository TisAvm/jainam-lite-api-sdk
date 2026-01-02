"""
Order Report API for Jainam Lite API

Handles retrieving order book (all orders).
"""

from typing import Dict, Any

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class OrderReportAPI:
    """
    Order report (order book) API handler.
    
    Retrieves all orders placed during the trading session.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize OrderReportAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def get_order_book(self) -> Dict[str, Any]:
        """
        Get all orders (order book).
        
        Returns all orders including open, complete, cancelled, and rejected.
        
        Returns:
            Response with list of orders containing:
            - brokerOrderId, exchangeOrderId
            - tradingSymbol, instrumentId, exchange
            - transactionType, quantity, price
            - orderStatus, filledQuantity, pendingQuantity
            - orderTime, exchangeUpdateTime
            
        Example:
            >>> order_report.get_order_book()
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "clientId": "DK2200295",
                    "brokerOrderId": "250526000002881",
                    "exchange": "NSE",
                    "tradingSymbol": "IDEA-EQ",
                    "transactionType": "BUY",
                    "quantity": 10,
                    "price": 6.30,
                    "orderStatus": "OPEN",
                    ...
                }]
            }
        """
        return self.client.get(urls.ORDER_BOOK)
