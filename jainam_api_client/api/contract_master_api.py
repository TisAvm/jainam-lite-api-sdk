"""
Contract Master API for Jainam Lite API

Handles downloading contract/scrip master files.
"""

import io
import json
import zipfile
from typing import Dict, Any, Optional

import pandas as pd

from jainam_api_client.rest import RestClient
from jainam_api_client import urls


class ContractMasterAPI:
    """
    Contract Master API handler.
    
    Downloads contract master files for all exchanges.
    Updated daily at 08:00 AM IST.
    
    Supported exchanges:
    - NSE: National Stock Exchange (Equities)
    - NFO: NSE Futures & Options
    - BSE: Bombay Stock Exchange
    - BFO: BSE Futures & Options
    - MCX: Multi Commodity Exchange
    - CDS: Currency Derivatives Segment
    - BCD: BSE Currency Derivatives
    - INDICES: Index data
    """
    
    def __init__(self, client: RestClient):
        """
        Initialize ContractMasterAPI.
        
        Args:
            client: REST client instance
        """
        self.client = client
    
    def get_contract_master(self, exchange: str) -> Dict[str, Any]:
        """
        Download contract master JSON for an exchange.
        
        Args:
            exchange: Exchange code (lowercase):
                nse, nfo, bse, bfo, mcx, cds, bcd, indices
                
        Returns:
            Parsed JSON contract data
            
        Example:
            >>> contracts = contract_master.get_contract_master("nse")
            >>> print(contracts[:2])
            [
                {"token": "26000", "symbol": "NIFTY 50", ...},
                {"token": "26009", "symbol": "NIFTY BANK", ...}
            ]
        """
        exchange = exchange.lower()
        if exchange not in urls.CONTRACT_URLS:
            raise ValueError(
                f"Invalid exchange: {exchange}. "
                f"Valid options: {list(urls.CONTRACT_URLS.keys())}"
            )
        
        url = urls.CONTRACT_URLS[exchange]
        content = self.client.download(url)
        
        # Content may be zipped
        try:
            # Try to unzip if it's a zip file
            with zipfile.ZipFile(io.BytesIO(content)) as zf:
                # Get the first file in the zip
                filename = zf.namelist()[0]
                with zf.open(filename) as f:
                    return json.load(f)
        except zipfile.BadZipFile:
            # Not a zip file, parse as JSON directly
            return json.loads(content)
    
    def get_contract_master_df(self, exchange: str) -> pd.DataFrame:
        """
        Download contract master as pandas DataFrame.
        
        Args:
            exchange: Exchange code (lowercase)
                
        Returns:
            DataFrame with contract data
        """
        data = self.get_contract_master(exchange)
        return pd.DataFrame(data)
    
    def search_symbol(
        self,
        exchange: str,
        symbol: str,
        expiry: Optional[str] = None,
        option_type: Optional[str] = None,
        strike_price: Optional[float] = None,
    ) -> pd.DataFrame:
        """
        Search for instruments in contract master.
        
        Args:
            exchange: Exchange code
            symbol: Trading symbol to search
            expiry: Expiry date filter (optional)
            option_type: CE or PE for options (optional)
            strike_price: Strike price filter (optional)
            
        Returns:
            DataFrame with matching instruments
        """
        df = self.get_contract_master_df(exchange)
        
        # Filter by symbol
        mask = df['symbol'].str.contains(symbol, case=False, na=False)
        
        if expiry:
            mask &= df['expiry'].str.contains(expiry, case=False, na=False)
        
        if option_type:
            mask &= df['optionType'] == option_type.upper()
        
        if strike_price is not None:
            mask &= df['strikePrice'] == strike_price
        
        return df[mask]
    
    def get_instrument_token(
        self,
        exchange: str,
        symbol: str,
    ) -> Optional[str]:
        """
        Get instrument token for a symbol.
        
        Args:
            exchange: Exchange code
            symbol: Trading symbol
            
        Returns:
            Instrument token or None if not found
        """
        df = self.get_contract_master_df(exchange)
        matches = df[df['symbol'] == symbol]
        
        if len(matches) > 0:
            return str(matches.iloc[0].get('token') or matches.iloc[0].get('instrumentId'))
        return None
