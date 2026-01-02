"""
Order Cancellation API for Jainam Lite API

Handles cancelling existing orders.
"""

from typing import Dict, Any

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class CancelOrderAPI:
    """
    Order cancellation API handler.
    
    Only open/pending orders can be cancelled.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize CancelOrderAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def cancel_order(self, broker_order_id: str) -> Dict[str, Any]:
        """
        Cancel an existing order.
        
        Args:
            broker_order_id: Order ID to cancel
            
        Returns:
            Response with brokerOrderId and requestTime
            
        Example:
            >>> cancel_api.cancel_order("250526000002881")
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "brokerOrderId": "250526000002881",
                    "requestTime": "26-May-2025 14:24:36"
                }]
            }
        """
        payload = {
            "brokerOrderId": broker_order_id,
        }
        return self.client.post(urls.CANCEL_ORDER, payload)
