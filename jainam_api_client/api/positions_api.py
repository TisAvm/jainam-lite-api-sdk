"""
Positions API for Jainam Lite API

Handles retrieving open positions.
"""

from typing import Dict, Any, List, Optional

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class PositionsAPI:
    """
    Positions API handler.
    
    Retrieves all open positions including F&O carryforward positions.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize PositionsAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def get_positions(self) -> Dict[str, Any]:
        """
        Get all open positions.
        
        Returns day and net positions including:
        - Intraday positions
        - Carryforward (overnight) positions
        - F&O positions
        
        Returns:
            Response with list of positions containing:
            - instrumentId, tradingSymbol, exchange
            - product, netQuantity, netAveragePrice
            - buyQuantity, sellQuantity
            - dayBuyQuantity, daySellQuantity
            - dayBuyPrice, daySellPrice
            - overnightQuantity, overnightPrice
            - realizedPnl, previousDayClose
            
        Example:
            >>> positions.get_positions()
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "instrumentId": "20776",
                    "tradingSymbol": "BHAGYANGR-EQ",
                    "exchange": "NSE",
                    "product": "LONGTERM",
                    "netQuantity": 1,
                    "netAveragePrice": 78.14,
                    ...
                }]
            }
        """
        return self.client.get(urls.POSITIONS)
    
    def square_off(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Square off (close) open positions.
        
        Places opposite orders to close the given positions.
        
        Args:
            positions: List of position dictionaries with order details:
                - exchange, instrumentId
                - transactionType (opposite to position)
                - quantity, product
                - orderComplexity, orderType
                - price (for LIMIT orders), validity
                
        Returns:
            Response with brokerOrderIds for square-off orders
            
        Example:
            >>> positions.square_off([{
            ...     "exchange": "NSE",
            ...     "instrumentId": "14366",
            ...     "transactionType": "SELL",  # Opposite to close
            ...     "quantity": 10,
            ...     "product": "LONGTERM",
            ...     "orderComplexity": "REGULAR",
            ...     "orderType": "MARKET",
            ...     "validity": "DAY"
            ... }])
        """
        return self.client.post(urls.SQUARE_OFF, positions)
