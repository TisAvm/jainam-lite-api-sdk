"""
Jainam Lite API Python SDK

Main API client class that provides access to all Jainam trading API endpoints.
"""

from typing import Dict, Any, Optional, List

from jainam_api_client.rest import RestClient
from jainam_api_client.urls import BASE_URL
from jainam_api_client.websocket import JainamWebSocket
from jainam_api_client.api import (
    AuthAPI,
    OrderAPI,
    ModifyOrderAPI,
    CancelOrderAPI,
    OrderReportAPI,
    OrderHistoryAPI,
    TradeReportAPI,
    PositionsAPI,
    HoldingsAPI,
    FundsAPI,
    MarginAPI,
    ProfileAPI,
    ContractMasterAPI,
)


class JainamAPI:
    """
    Main client for Jainam Lite Trading API.
    
    This is the primary interface for interacting with Jainam's trading platform.
    It provides access to:
    - Authentication (SSO vendor flow)
    - Order Management (place, modify, cancel)
    - Order/Trade Information (order book, trade book, history)
    - Portfolio (positions, holdings)
    - Account (funds/limits, profile, margin)
    - Market Data (contract master, WebSocket streaming)
    
    Usage:
        >>> from jainam_api_client import JainamAPI
        >>> 
        >>> # Initialize client
        >>> client = JainamAPI()
        >>> 
        >>> # Authenticate via SSO
        >>> client.login_with_sso(
        ...     user_id="DK2200295",
        ...     auth_code="your_auth_code",
        ...     api_secret="your_api_secret",
        ...     app_code="your_app_code"
        ... )
        >>> 
        >>> # Place an order
        >>> client.place_order(
        ...     exchange="NSE",
        ...     instrument_id="14366",
        ...     transaction_type="BUY",
        ...     quantity=10,
        ...     order_type="LIMIT",
        ...     price="6.3"
        ... )
        >>> 
        >>> # Get order book
        >>> orders = client.order_report()
        >>> 
        >>> # Get positions
        >>> positions = client.positions()
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Jainam API client.
        
        Args:
            access_token: Optional JWT access token if already authenticated
        """
        self._rest_client = RestClient(BASE_URL)
        self._user_id: Optional[str] = None
        self._session_id: Optional[str] = None
        self._websocket: Optional[JainamWebSocket] = None
        
        # Initialize API handlers
        self._auth = AuthAPI(self._rest_client)
        self._order = OrderAPI(self._rest_client)
        self._modify_order = ModifyOrderAPI(self._rest_client)
        self._cancel_order = CancelOrderAPI(self._rest_client)
        self._order_report = OrderReportAPI(self._rest_client)
        self._order_history = OrderHistoryAPI(self._rest_client)
        self._trade_report = TradeReportAPI(self._rest_client)
        self._positions = PositionsAPI(self._rest_client)
        self._holdings = HoldingsAPI(self._rest_client)
        self._funds = FundsAPI(self._rest_client)
        self._margin = MarginAPI(self._rest_client)
        self._profile = ProfileAPI(self._rest_client)
        self._contract_master = ContractMasterAPI(self._rest_client)
        
        # WebSocket callbacks
        self.on_message = None
        self.on_error = None
        self.on_close = None
        self.on_open = None
        
        # Set token if provided
        if access_token:
            self.set_access_token(access_token)
    
    # ==================== Authentication ====================
    
    def login_with_sso(
        self,
        user_id: str,
        auth_code: str,
        api_secret: str,
        app_code: str
    ) -> Dict[str, Any]:
        """
        Authenticate using SSO vendor flow.
        
        After user is redirected back from Jainam login, use the authCode
        and userId to get a session token.
        
        Args:
            user_id: User ID from redirect callback
            auth_code: Authorization code from redirect callback
            api_secret: Your API secret from developer portal
            app_code: Your App Code from developer portal
            
        Returns:
            Response containing userSession token
        """
        response = self._auth.get_user_session(
            user_id=user_id,
            auth_code=auth_code,
            api_secret=api_secret,
            app_code=app_code
        )
        
        # Extract and set session token
        if response.get("status") == "Ok":
            result = response.get("result", {})
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
            
            # API returns accessToken (not userSession)
            session_token = result.get("accessToken") or result.get("userSession")
            if session_token:
                self._user_id = user_id
                self._session_id = session_token
                self.set_access_token(session_token)
        
        return response
    
    def set_access_token(self, token: str):
        """
        Set access token for API authentication.
        
        Args:
            token: JWT access token
        """
        self._rest_client.set_access_token(token)
    
    def logout(self):
        """Clear session and disconnect WebSocket."""
        self._rest_client.clear_token()
        self._user_id = None
        self._session_id = None
        
        if self._websocket:
            self._websocket.disconnect()
            self._websocket = None
    
    # ==================== Order Management ====================
    
    def place_order(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        product: str = "LONGTERM",
        order_complexity: str = "REGULAR",
        order_type: str = "LIMIT",
        price: Optional[str] = None,
        validity: str = "DAY",
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
            exchange: Exchange code (NSE, BSE, NFO, BFO, MCX, CDS)
            instrument_id: Unique instrument ID from contract master
            transaction_type: BUY or SELL
            quantity: Order quantity
            product: INTRADAY, LONGTERM, or MTF (default: LONGTERM)
            order_complexity: REGULAR or AMO (default: REGULAR)
            order_type: LIMIT, MARKET, SL, SLM (default: LIMIT)
            price: Order price (required for LIMIT orders)
            validity: DAY or IOC (default: DAY)
            sl_trigger_price: Stop loss trigger price
            trailing_sl_amount: Trailing stop loss amount
            disclosed_quantity: Quantity to disclose
            market_protection_percent: Market protection %
            api_order_source: API source identifier
            algo_id: Algorithm ID (max 12 chars)
            order_tag: Custom tag (max 50 chars)
            
        Returns:
            Response with brokerOrderId
        """
        return self._order.place_order(
            exchange=exchange,
            instrument_id=instrument_id,
            transaction_type=transaction_type,
            quantity=quantity,
            product=product,
            order_complexity=order_complexity,
            order_type=order_type,
            price=price,
            validity=validity,
            sl_trigger_price=sl_trigger_price,
            trailing_sl_amount=trailing_sl_amount,
            disclosed_quantity=disclosed_quantity,
            market_protection_percent=market_protection_percent,
            api_order_source=api_order_source,
            algo_id=algo_id,
            order_tag=order_tag,
        )
    
    def place_market_order(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        product: str = "LONGTERM",
    ) -> Dict[str, Any]:
        """Place a market order."""
        return self._order.place_market_order(
            exchange=exchange,
            instrument_id=instrument_id,
            transaction_type=transaction_type,
            quantity=quantity,
            product=product,
        )
    
    def place_limit_order(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        price: str,
        product: str = "LONGTERM",
    ) -> Dict[str, Any]:
        """Place a limit order."""
        return self._order.place_limit_order(
            exchange=exchange,
            instrument_id=instrument_id,
            transaction_type=transaction_type,
            quantity=quantity,
            price=price,
            product=product,
        )
    
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
        
        Args:
            broker_order_id: Order ID to modify
            quantity: New quantity (optional)
            order_type: New order type (optional)
            price: New price (optional)
            sl_trigger_price: New trigger price (optional)
            validity: New validity (optional)
            disclosed_quantity: New disclosed qty (optional)
            market_protection_percent: New market protection (optional)
            trailing_sl_amount: New trailing SL (optional)
            
        Returns:
            Response with modification status
        """
        return self._modify_order.modify_order(
            broker_order_id=broker_order_id,
            quantity=quantity,
            order_type=order_type,
            price=price,
            sl_trigger_price=sl_trigger_price,
            validity=validity,
            disclosed_quantity=disclosed_quantity,
            market_protection_percent=market_protection_percent,
            trailing_sl_amount=trailing_sl_amount,
        )
    
    def cancel_order(self, broker_order_id: str) -> Dict[str, Any]:
        """
        Cancel an existing order.
        
        Args:
            broker_order_id: Order ID to cancel
            
        Returns:
            Response with cancellation status
        """
        return self._cancel_order.cancel_order(broker_order_id)
    
    # ==================== Order Information ====================
    
    def order_report(self) -> Dict[str, Any]:
        """
        Get order book (all orders).
        
        Returns:
            Response with list of orders
        """
        return self._order_report.get_order_book()
    
    def order_history(self, broker_order_id: str) -> Dict[str, Any]:
        """
        Get order history/audit trail.
        
        Args:
            broker_order_id: Order ID
            
        Returns:
            Response with order state transitions
        """
        return self._order_history.get_order_history(broker_order_id)
    
    def trade_report(self) -> Dict[str, Any]:
        """
        Get trade book (executed trades).
        
        Returns:
            Response with list of trades
        """
        return self._trade_report.get_trade_book()
    
    # ==================== Portfolio ====================
    
    def positions(self) -> Dict[str, Any]:
        """
        Get open positions.
        
        Returns:
            Response with list of positions
        """
        return self._positions.get_positions()
    
    def square_off(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Square off (close) positions.
        
        Args:
            positions: List of position orders
            
        Returns:
            Response with square-off order IDs
        """
        return self._positions.square_off(positions)
    
    def holdings(self, product_type: str = "cnc") -> Dict[str, Any]:
        """
        Get portfolio holdings.
        
        Args:
            product_type: "cnc" (LONGTERM), "mtf", or "mis" (INTRADAY)
            
        Returns:
            Response with list of holdings
        """
        return self._holdings.get_holdings(product_type)
    
    # ==================== Account ====================
    
    def limits(self) -> Dict[str, Any]:
        """
        Get account funds and limits.
        
        Returns:
            Response with fund details
        """
        return self._funds.get_limits()
    
    def profile(self) -> Dict[str, Any]:
        """
        Get user profile.
        
        Returns:
            Response with profile details
        """
        return self._profile.get_profile()
    
    def margin_required(
        self,
        exchange: str,
        instrument_id: str,
        transaction_type: str,
        quantity: int,
        product: str,
        order_type: str = "MARKET",
        price: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Check margin required for an order.
        
        Args:
            exchange: Exchange code
            instrument_id: Instrument ID
            transaction_type: BUY or SELL
            quantity: Order quantity
            product: Product type
            order_type: Order type (default: MARKET)
            price: Price (for LIMIT orders)
            
        Returns:
            Response with margin details
        """
        return self._margin.check_margin(
            exchange=exchange,
            instrument_id=instrument_id,
            transaction_type=transaction_type,
            quantity=quantity,
            product=product,
            order_type=order_type,
            price=price,
        )
    
    # ==================== Market Data ====================
    
    def contract_master(self, exchange: str) -> Dict[str, Any]:
        """
        Download contract master for an exchange.
        
        Args:
            exchange: Exchange code (nse, nfo, bse, bfo, mcx, cds, bcd, indices)
            
        Returns:
            Contract master data as JSON
        """
        return self._contract_master.get_contract_master(exchange)
    
    def search_symbol(
        self,
        exchange: str,
        symbol: str,
        expiry: Optional[str] = None,
        option_type: Optional[str] = None,
        strike_price: Optional[float] = None,
    ):
        """
        Search for instruments in contract master.
        
        Args:
            exchange: Exchange code
            symbol: Symbol to search
            expiry: Expiry filter (optional)
            option_type: CE or PE (optional)
            strike_price: Strike price filter (optional)
            
        Returns:
            DataFrame with matching instruments
        """
        return self._contract_master.search_symbol(
            exchange=exchange,
            symbol=symbol,
            expiry=expiry,
            option_type=option_type,
            strike_price=strike_price,
        )
    
    # ==================== WebSocket ====================
    
    def create_websocket_session(self) -> Dict[str, Any]:
        """Create WebSocket session."""
        if not self._user_id or not self._session_id:
            raise Exception("Not authenticated. Call login_with_sso first.")
        
        return self._auth.create_websocket_session(
            user_id=self._user_id,
            token=self._session_id
        )
    
    def subscribe(
        self,
        instruments: List[Dict[str, str]],
        is_depth: bool = False
    ):
        """
        Subscribe to market data via WebSocket.
        
        Args:
            instruments: List of dicts with 'exchange' and 'token' keys
            is_depth: If True, subscribe to depth data
            
        Example:
            >>> client.on_message = lambda msg: print(msg)
            >>> client.subscribe([
            ...     {"exchange": "NSE", "token": "26000"},
            ...     {"exchange": "NFO", "token": "54957"}
            ... ])
        """
        if not self._websocket:
            if not self._user_id or not self._session_id:
                raise Exception("Not authenticated. Call login_with_sso first.")
            
            # Create WebSocket and set callbacks
            self._websocket = JainamWebSocket(
                user_id=self._user_id,
                session_id=self._session_id
            )
            self._websocket.on_message = self.on_message
            self._websocket.on_error = self.on_error
            self._websocket.on_close = self.on_close
            self._websocket.on_open = self.on_open
            
            # Connect
            self._websocket.connect()
            
            # Wait for connection
            import time
            for _ in range(10):
                if self._websocket.connected:
                    break
                time.sleep(0.5)
        
        self._websocket.subscribe(instruments, is_depth=is_depth)
    
    def unsubscribe(
        self,
        instruments: List[Dict[str, str]],
        is_depth: bool = False
    ):
        """
        Unsubscribe from market data.
        
        Args:
            instruments: List of dicts with 'exchange' and 'token' keys
            is_depth: If True, unsubscribe from depth data
        """
        if self._websocket:
            self._websocket.unsubscribe(instruments, is_depth=is_depth)
