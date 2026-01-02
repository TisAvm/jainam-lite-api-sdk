"""
Order History API for Jainam Lite API

Handles retrieving order history for specific orders.
"""

from typing import Dict, Any

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class OrderHistoryAPI:
    """
    Order history API handler.
    
    Retrieves the complete history/audit trail for a specific order.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize OrderHistoryAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def get_order_history(self, broker_order_id: str) -> Dict[str, Any]:
        """
        Get history/audit trail for a specific order.
        
        Shows all state transitions for the order:
        - validation pending
        - put order req received
        - open pending
        - open
        - complete/cancelled/rejected
        
        Args:
            broker_order_id: Order ID to get history for
            
        Returns:
            Response with list of order state transitions
            
        Example:
            >>> order_history.get_order_history("250526000002881")
            {
                "status": "Ok",
                "message": "Success",
                "result": [
                    {"orderStatus": "open", ...},
                    {"orderStatus": "open pending", ...},
                    {"orderStatus": "validation pending", ...},
                    {"orderStatus": "put order req received", ...}
                ]
            }
        """
        payload = {
            "brokerOrderId": broker_order_id,
        }
        return self.client.post(urls.ORDER_HISTORY, payload)
