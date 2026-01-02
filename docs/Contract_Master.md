# Contract Master

Download contract master data.

```python
client.contract_master(exchange="nse")
```

## Example

```python
from jainam_api_client import JainamAPI

client = JainamAPI()

# Download contract master (no auth required)
nse = client.contract_master("nse")
nfo = client.contract_master("nfo")

# Search for instruments
results = client.search_symbol(
    exchange="nfo",
    symbol="NIFTY",
    expiry="26DEC",
    option_type="CE",
    strike_price=24000
)
print(results)
```

## Parameters

| Name | Description | Type |
|------|-------------|------|
| *exchange* | nse, nfo, bse, bfo, mcx, cds, bcd, indices | Str (required) |

## Available Exchanges

| Exchange | Description |
|----------|-------------|
| nse | NSE Cash Segment |
| nfo | NSE Futures & Options |
| bse | BSE Cash Segment |
| bfo | BSE Futures & Options |
| mcx | Multi Commodity Exchange |
| cds | Currency Derivatives |
| bcd | BSE Currency Derivatives |
| indices | Index Data |

## Contract Data Fields

| Field | Description |
|-------|-------------|
| token | Instrument token |
| symbol | Trading symbol |
| expiry | Expiry date (for derivatives) |
| strikePrice | Strike price (for options) |
| optionType | CE or PE (for options) |
| lotSize | Lot size |

## Download URLs

Contract files are updated daily at 08:00 AM IST:
- `https://protrade.jainam.in/contract/json/nse`
- `https://protrade.jainam.in/contract/json/nfo`
- `https://protrade.jainam.in/contract/json/bse`
- `https://protrade.jainam.in/contract/json/bfo`
- `https://protrade.jainam.in/contract/json/mcx`
- `https://protrade.jainam.in/contract/json/cds`
- `https://protrade.jainam.in/contract/json/bcd`
- `https://protrade.jainam.in/contract/json/indices`

[[Back to top]](#) [[Back to README]](../README.md)
