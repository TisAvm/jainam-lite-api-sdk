"""
Order Placement API for Jainam Lite API

Handles placing new orders.
"""

from typing import Dict, Any, Optional, List

from jainam_api_client.rest import RestClient
from jainam_api_client import urls
from jainam_api_client.settings import (
    ORDER_TYPE_LIMIT,
    ORDER_TYPE_MARKET,
    PRODUCT_LONGTERM,
    COMPLEXITY_REGULAR,
    VALIDITY_DAY,
)


class OrderAPI:
    """
    Order placement API handler.
    
    Supports placing:
    - Regular orders (LIMIT, MARKET, SL, SLM)
    - AMO (After Market Orders)
    - Various product types (INTRADAY, LONGTERM, MTF)
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize OrderAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def place_order(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        product: str = PRODUCT_LONGTERM,
        order_complexity: str = COMPLEXITY_REGULAR,
        order_type: str = ORDER_TYPE_LIMIT,
        price: Optional[str] = None,
        validity: str = VALIDITY_DAY,
        sl_trigger_price: Optional[str] = None,
        trailing_sl_amount: Optional[str] = None,
        disclosed_quantity: Optional[int] = None,
        market_protection_percent: Optional[str] = None,
        api_order_source: Optional[str] = None,
        algo_id: Optional[str] = None,
        order_tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Place a new order.
        
        Args:
            exchange: Exchange code (NSE, BSE, NFO, BFO, MCX, CDS, etc.)
            instrument_id: Unique instrument identifier from contract master
            transaction_type: BUY or SELL
            quantity: Order quantity
            product: Product type - INTRADAY, LONGTERM, MTF (default: LONGTERM)
            order_complexity: REGULAR or AMO (default: REGULAR)
            order_type: LIMIT, MARKET, SL, SLM (default: LIMIT)
            price: Order price (required for LIMIT and SL orders)
            validity: DAY or IOC (default: DAY)
            sl_trigger_price: Stop loss trigger price (required for SL/SLM)
            trailing_sl_amount: Trailing stop loss amount
            disclosed_quantity: Quantity to disclose to market
            market_protection_percent: Market protection percentage
            api_order_source: Source identifier for API orders
            algo_id: Algorithm identifier (max 12 chars)
            order_tag: Custom tag to identify orders (max 50 chars)
            
        Returns:
            Response with brokerOrderId and requestTime
            
        Example:
            >>> order_api.place_order(
            ...     exchange="NSE",
            ...     instrument_id="14366",
            ...     transaction_type="BUY",
            ...     quantity=10,
            ...     product="LONGTERM",
            ...     order_type="LIMIT",
            ...     price="6.3",
            ...     validity="DAY"
            ... )
            {
                "status": "Ok",
                "message": "Success",
                "result": [{
                    "requestTime": "26-May-2025 11:42:10",
                    "brokerOrderId": "250526000002697"
                }]
            }
        """
        order_data = {
            "exchange": exchange,
            "instrumentId": instrument_id,
            "transactionType": transaction_type,
            "quantity": quantity,
            "product": product,
            "orderComplexity": order_complexity,
            "orderType": order_type,
            "validity": validity,
            "price": price or "",
            "slTriggerPrice": sl_trigger_price or "",
            "trailingSlAmount": trailing_sl_amount or "",
            "disclosedQuantity": disclosed_quantity if disclosed_quantity else "",
            "marketProtectionPercent": market_protection_percent or "",
            "apiOrderSource": api_order_source or "",
            "algoId": algo_id or "",
            "orderTag": order_tag or "",
        }
        
        # API expects array of orders
        return self.client.post(urls.PLACE_ORDER, [order_data])
    
    def place_orders(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Place multiple orders at once.
        
        Args:
            orders: List of order dictionaries with keys:
                - exchange, instrumentId, transactionType, quantity
                - product, orderComplexity, orderType, validity
                - price, slTriggerPrice, etc. (optional)
                
        Returns:
            Response with list of brokerOrderIds
        """
        return self.client.post(urls.PLACE_ORDER, orders)
    
    def place_market_order(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        product: str = PRODUCT_LONGTERM,
    ) -> Dict[str, Any]:
        """
        Convenience method to place a market order.
        
        Args:
            exchange: Exchange code
            instrument_id: Instrument identifier
            transaction_type: BUY or SELL
            quantity: Order quantity
            product: Product type (default: LONGTERM)
            
        Returns:
            Response with brokerOrderId
        """
        return self.place_order(
            exchange=exchange,
            instrument_id=instrument_id,
            transaction_type=transaction_type,
            quantity=quantity,
            product=product,
            order_type=ORDER_TYPE_MARKET,
        )
    
    def place_limit_order(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        price: str,
        product: str = PRODUCT_LONGTERM,
    ) -> Dict[str, Any]:
        """
        Convenience method to place a limit order.
        
        Args:
            exchange: Exchange code
            instrument_id: Instrument identifier
            transaction_type: BUY or SELL
            quantity: Order quantity
            price: Limit price
            product: Product type (default: LONGTERM)
            
        Returns:
            Response with brokerOrderId
        """
        return self.place_order(
            exchange=exchange,
            instrument_id=instrument_id,
            transaction_type=transaction_type,
            quantity=quantity,
            price=price,
            product=product,
            order_type=ORDER_TYPE_LIMIT,
        )
    
    def place_sl_order(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        price: str,
        trigger_price: str,
        product: str = PRODUCT_LONGTERM,
    ) -> Dict[str, Any]:
        """
        Convenience method to place a stop loss order.
        
        Args:
            exchange: Exchange code
            instrument_id: Instrument identifier
            transaction_type: BUY or SELL
            quantity: Order quantity
            price: Limit price
            trigger_price: Stop loss trigger price
            product: Product type (default: LONGTERM)
            
        Returns:
            Response with brokerOrderId
        """
        return self.place_order(
            exchange=exchange,
            instrument_id=instrument_id,
            transaction_type=transaction_type,
            quantity=quantity,
            price=price,
            sl_trigger_price=trigger_price,
            product=product,
            order_type="SL",
        )
