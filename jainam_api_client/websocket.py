"""
WebSocket Client for Jainam Lite API

Handles real-time market data streaming.
"""

import hashlib
import json
import threading
import time
from typing import Callable, Dict, Any, List, Optional

import websocket

from jainam_api_client.urls import WEBSOCKET_URL
from jainam_api_client.settings import (
    WS_TYPE_CONNECT,
    WS_TYPE_HEARTBEAT,
    WS_TYPE_TICK,
    WS_TYPE_DEPTH,
    WS_TYPE_UNSUBSCRIBE,
    WS_TYPE_UNSUBSCRIBE_DEPTH,
)


class JainamWebSocket:
    """
    WebSocket client for real-time market data.
    
    Features:
    - Market data subscription (LTP, OHLC, Volume)
    - Depth data subscription (bid/ask prices and quantities)
    - Automatic heartbeat to keep connection alive
    - Callback-based event handling
    
    Usage:
        >>> ws = JainamWebSocket(user_id="DK2200295", session_id="your_session")
        >>> ws.on_message = lambda msg: print(msg)
        >>> ws.connect()
        >>> ws.subscribe([{"exchange": "NSE", "token": "26000"}])
    """
    
    def __init__(self, user_id: str, session_id: str):
        """
        Initialize WebSocket client.
        
        Args:
            user_id: User ID (will be suffixed with _API)
            session_id: Session ID (will be double SHA-256 hashed)
        """
        self.user_id = f"{user_id}_API"
        self.session_id = session_id
        self.susertoken = self._create_susertoken(session_id)
        
        self.ws: Optional[websocket.WebSocketApp] = None
        self.ws_thread: Optional[threading.Thread] = None
        self.heartbeat_thread: Optional[threading.Thread] = None
        self.connected = False
        self.subscribed_tokens: set = set()
        
        # Callbacks
        self.on_message: Optional[Callable[[Dict], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        self.on_close: Optional[Callable[[str], None]] = None
        self.on_open: Optional[Callable[[], None]] = None
    
    def _create_susertoken(self, session_id: str) -> str:
        """
        Create susertoken by double SHA-256 hashing session ID.
        
        Args:
            session_id: Original session ID
            
        Returns:
            Double SHA-256 hex digest
        """
        # First hash
        first_hash = hashlib.sha256(session_id.encode()).hexdigest()
        # Second hash
        second_hash = hashlib.sha256(first_hash.encode()).hexdigest()
        return second_hash
    
    def _format_instruments(self, instruments: List[Dict[str, str]]) -> str:
        """
        Format instruments for subscription request.
        
        Args:
            instruments: List of dicts with 'exchange' and 'token' keys
            
        Returns:
            Formatted string like "NSE|26000#BSE|1"
        """
        formatted = []
        for inst in instruments:
            exchange = inst.get("exchange", "").upper()
            token = inst.get("token", "")
            formatted.append(f"{exchange}|{token}")
        return "#".join(formatted)
    
    def _on_message(self, ws, message: str):
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(message)
            
            # Check connection status
            if data.get("t") == "cf":
                if data.get("s") == "OK":
                    self.connected = True
                    self._start_heartbeat()
            
            if self.on_message:
                self.on_message(data)
        except json.JSONDecodeError:
            if self.on_error:
                self.on_error(Exception(f"Invalid JSON: {message}"))
    
    def _on_error(self, ws, error):
        """Handle WebSocket error."""
        if self.on_error:
            self.on_error(error)
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close."""
        self.connected = False
        if self.on_close:
            self.on_close(f"Connection closed: {close_status_code} - {close_msg}")
    
    def _on_open(self, ws):
        """Handle WebSocket connection open."""
        # Send connection request
        connect_msg = {
            "susertoken": self.susertoken,
            "t": WS_TYPE_CONNECT,
            "actid": self.user_id,
            "uid": self.user_id,
            "source": "API",
        }
        ws.send(json.dumps(connect_msg))
        
        if self.on_open:
            self.on_open()
    
    def _start_heartbeat(self):
        """Start heartbeat thread to keep connection alive."""
        def heartbeat_loop():
            while self.connected:
                time.sleep(50)  # Send heartbeat every 50 seconds
                if self.connected and self.ws:
                    self.send_heartbeat()
        
        self.heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
    
    def connect(self):
        """
        Connect to WebSocket server.
        
        Starts the WebSocket connection in a background thread.
        """
        self.ws = websocket.WebSocketApp(
            WEBSOCKET_URL,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )
        
        self.ws_thread = threading.Thread(
            target=self.ws.run_forever,
            daemon=True
        )
        self.ws_thread.start()
    
    def disconnect(self):
        """Disconnect from WebSocket server."""
        self.connected = False
        if self.ws:
            self.ws.close()
    
    def send_heartbeat(self):
        """Send heartbeat to keep connection alive."""
        if self.ws and self.connected:
            msg = {"k": "", "t": WS_TYPE_HEARTBEAT}
            self.ws.send(json.dumps(msg))
    
    def subscribe(
        self,
        instruments: List[Dict[str, str]],
        is_depth: bool = False
    ):
        """
        Subscribe to market data for instruments.
        
        Args:
            instruments: List of dicts with 'exchange' and 'token' keys
            is_depth: If True, subscribe to depth data (5-level)
            
        Example:
            >>> ws.subscribe([
            ...     {"exchange": "NSE", "token": "26000"},
            ...     {"exchange": "NFO", "token": "54957"}
            ... ])
        """
        if not self.ws or not self.connected:
            raise Exception("WebSocket not connected")
        
        formatted = self._format_instruments(instruments)
        msg_type = WS_TYPE_DEPTH if is_depth else WS_TYPE_TICK
        
        msg = {"k": formatted, "t": msg_type}
        self.ws.send(json.dumps(msg))
        
        # Track subscribed tokens
        for inst in instruments:
            self.subscribed_tokens.add(f"{inst['exchange']}|{inst['token']}")
    
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
        if not self.ws or not self.connected:
            raise Exception("WebSocket not connected")
        
        formatted = self._format_instruments(instruments)
        msg_type = WS_TYPE_UNSUBSCRIBE_DEPTH if is_depth else WS_TYPE_UNSUBSCRIBE
        
        msg = {"k": formatted, "t": msg_type}
        self.ws.send(json.dumps(msg))
        
        # Remove from tracked tokens
        for inst in instruments:
            self.subscribed_tokens.discard(f"{inst['exchange']}|{inst['token']}")
    
    def subscribe_tick(self, instruments: List[Dict[str, str]]):
        """
        Subscribe to tick data (LTP, OHLC, Volume).
        
        Args:
            instruments: List of dicts with 'exchange' and 'token' keys
        """
        self.subscribe(instruments, is_depth=False)
    
    def subscribe_depth(self, instruments: List[Dict[str, str]]):
        """
        Subscribe to depth data (5-level bid/ask).
        
        Args:
            instruments: List of dicts with 'exchange' and 'token' keys
        """
        self.subscribe(instruments, is_depth=True)


# WebSocket message field mappings for reference
WS_FIELD_MAPPING = {
    "t": "type",           # tf=tick feed, tk=tick ack, df=depth feed, dk=depth ack
    "e": "exchange",
    "tk": "token",
    "lp": "ltp",           # Last traded price
    "pc": "percent_change",
    "cv": "change_value",
    "v": "volume",
    "o": "open",
    "h": "high",
    "l": "low",
    "c": "close",
    "ap": "average_price",
    "ts": "symbol",
    "oi": "open_interest",
    "ltq": "last_traded_qty",
    "ltt": "last_traded_time",
    "tbq": "total_buy_qty",
    "tsq": "total_sell_qty",
    "uc": "upper_circuit",
    "lc": "lower_circuit",
    # Depth fields (1-5)
    "bp1": "bid_price_1", "sp1": "ask_price_1",
    "bq1": "bid_qty_1", "sq1": "ask_qty_1",
    "bo1": "bid_orders_1", "so1": "ask_orders_1",
    # ... up to bp5, sp5, etc.
}
