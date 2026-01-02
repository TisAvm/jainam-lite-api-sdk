"""
Order Modification API for Jainam Lite API

Handles modifying existing orders.
"""

from typing import Dict, Any, Optional

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class ModifyOrderAPI:
    """
    Order modification API handler.
    
    Allows modification of:
    - Quantity
    - Price
    - Order type
    - Trigger price (for SL orders)
    - Validity
    - Disclosed quantity
    - Market protection
    - Trailing stop loss
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize ModifyOrderAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def modify_order(
        self,
        broker_order_id: str,
        quantity: Optional[int] = None,
        order_type: Optional[str] = None,
        price: Optional[str] = None,
        sl_trigger_price: Optional[str] = None,
        validity: Optional[str] = None,
        disclosed_quantity: Optional[str] = None,
        market_protection_percent: Optional[str] = None,
        trailing_sl_amount: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Modify an existing order.
        
        Only open/pending orders can be modified.
        
        Args:
            broker_order_id: Order ID to modify (required)
            quantity: New quantity (optional)
            order_type: New order type - LIMIT, MARKET, SL, SLM (optional)
            price: New price (required for LIMIT orders)
            sl_trigger_price: New trigger price (required for SL/SLM orders)
            validity: New validity - DAY, IOC (optional)
            disclosed_quantity: New disclosed quantity (optional)
            market_protection_percent: New market protection % (optional)
            trailing_sl_amount: New trailing SL amount (optional)
            
        Returns:
            Response with brokerOrderId and requestTime
            
        Example:
            >>> modify_api.modify_order(
            ...     broker_order_id="250526000002881",
            ...     quantity=20,
            ...     price="6.5"
            ... )
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "brokerOrderId": "250526000002881",
                    "requestTime": "26-May-2025 13:11:34"
                }]
            }
        """
        payload = {
            "brokerOrderId": broker_order_id,
        }
        
        # Add optional parameters only if provided
        if quantity is not None:
            payload["quantity"] = quantity
        if order_type is not None:
            payload["orderType"] = order_type
        if price is not None:
            payload["price"] = price
        if sl_trigger_price is not None:
            payload["slTriggerPrice"] = sl_trigger_price
        if validity is not None:
            payload["validity"] = validity
        if disclosed_quantity is not None:
            payload["disclosedQuantity"] = disclosed_quantity
        if market_protection_percent is not None:
            payload["marketProtectionPercent"] = market_protection_percent
        if trailing_sl_amount is not None:
            payload["trailingSLAmount"] = trailing_sl_amount
        
        return self.client.post(urls.MODIFY_ORDER, payload)
    
    def modify_price(
        self,
        broker_order_id: str,
        price: str,
    ) -> Dict[str, Any]:
        """
        Convenience method to modify only the price.
        
        Args:
            broker_order_id: Order ID to modify
            price: New price
            
        Returns:
            Response with modification status
        """
        return self.modify_order(
            broker_order_id=broker_order_id,
            price=price,
        )
    
    def modify_quantity(
        self,
        broker_order_id: str,
        quantity: int,
    ) -> Dict[str, Any]:
        """
        Convenience method to modify only the quantity.
        
        Args:
            broker_order_id: Order ID to modify
            quantity: New quantity
            
        Returns:
            Response with modification status
        """
        return self.modify_order(
            broker_order_id=broker_order_id,
            quantity=quantity,
        )
