"""
Margin API for Jainam Lite API

Handles calculating margin required for orders.
"""

from typing import Dict, Any, Optional

from jainam_api_client.rest import RestClient
from jainam_api_client import urls
from jainam_api_client.settings import (
    COMPLEXITY_REGULAR,
    ORDER_TYPE_MARKET,
    VALIDITY_DAY,
)


class MarginAPI:
    """
    Margin API handler.
    
    Calculates margin required for placing orders.
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize MarginAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def check_margin(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        product: str,
        order_complexity: str = COMPLEXITY_REGULAR,
        order_type: str = ORDER_TYPE_MARKET,
        price: Optional[str] = None,
        validity: str = VALIDITY_DAY,
        sl_trigger_price: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Check margin required for an order.
        
        Calculate the margin required before placing an order.
        
        Args:
            exchange: Exchange code (NSE, BSE, NFO, etc.)
            instrument_id: Instrument identifier
            transaction_type: BUY or SELL
            quantity: Order quantity
            product: Product type (INTRADAY, LONGTERM)
            order_complexity: REGULAR or AMO (default: REGULAR)
            order_type: LIMIT, MARKET, SL, SLM (default: MARKET)
            price: Order price (for LIMIT orders)
            validity: DAY or IOC (default: DAY)
            sl_trigger_price: Trigger price (for SL orders)
            
        Returns:
            Response with margin details containing:
            - totalCashAvailable: Available cash
            - preOrderMargin: Margin before order
            - postOrderMargin: Margin after order
            - currentOrderMargin: Margin for this order
            - rmsValidationCheck: RMS validation status
            - fundShort: Fund shortfall if any
            
        Example:
            >>> margin.check_margin(
            ...     exchange="NSEEQ",
            ...     instrument_id="22",
            ...     transaction_type="BUY",
            ...     quantity=1,
            ...     product="intraday",
            ...     order_type="market"
            ... )
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "totalCashAvailable": "52926",
                    "postOrderMargin": "183.65",
                    "currentOrderMargin": "113.70",
                    ...
                }]
            }
        """
        payload = {
            "exchange": exchange,
            "instrumentId": instrument_id,
            "transactionType": transaction_type,
            "quantity": quantity,
            "product": product,
            "orderComplexity": order_complexity,
            "orderType": order_type,
            "price": price or "",
            "validity": validity,
            "slTriggerPrice": sl_trigger_price or "",
        }
        return self.client.post(urls.CHECK_MARGIN, payload)
