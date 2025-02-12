import requests
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import json
import time

class CoinAPIClient:
    """Client for interacting with CoinAPI to fetch BTC market data."""
    
    def __init__(self, api_key: str) -> None:
        """Initialize the CoinAPI client with API key."""
        self.api_key = api_key
        self.base_url = "https://rest.coinapi.io/v1"
        self.headers = {"X-CoinAPI-Key": api_key}
        self.base_delay = 10  # Increased to 10 seconds
        
        # Instead of getting all symbols, we'll directly query specific exchanges
        self.us_exchanges = ["COINBASE", "KRAKEN", "GEMINI"]
    
    def _make_request(self, endpoint: str) -> Dict:
        """Make a request to the API with conservative rate limiting."""
        url = f"{self.base_url}/{endpoint}"
        
        print(f"Waiting {self.base_delay} seconds before request...")
        time.sleep(self.base_delay)
        
        print(f"Making request to {endpoint}...")
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("\nAPI Rate limit reached. Using fallback data...")
            # Return minimal fallback data for testing
            if "exchanges" in endpoint:
                return self._get_fallback_exchanges()
            elif "symbols" in endpoint:
                return self._get_fallback_symbols(endpoint.split("=")[1].split("_")[0])
            else:
                raise requests.exceptions.RequestException(
                    "Rate limit exceeded - no fallback available"
                )
        else:
            response.raise_for_status()
    
    def _get_fallback_exchanges(self) -> List[Dict]:
        """Provide fallback exchange data when API limits are hit."""
        return [
            {"exchange_id": "COINBASE", "name": "Coinbase"},
            {"exchange_id": "KRAKEN", "name": "Kraken"},
            {"exchange_id": "GEMINI", "name": "Gemini"}
        ]
    
    def _get_fallback_symbols(self, exchange: str) -> List[Dict]:
        """Provide fallback symbol data when API limits are hit."""
        # Basic BTC pairs that are commonly available
        return [
            {
                "symbol_id": f"{exchange}_SPOT_BTC_USD",
                "exchange_id": exchange,
                "symbol_type": "SPOT",
                "asset_id_base": "BTC",
                "asset_id_quote": "USD",
                "volume_1day": 0,
                "volume_1month": 0,
                "price_precision": 2,
                "data_start": "2023-01-01",
                "data_end": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "symbol_id": f"{exchange}_SPOT_BTC_USDT",
                "exchange_id": exchange,
                "symbol_type": "SPOT",
                "asset_id_base": "BTC",
                "asset_id_quote": "USDT",
                "volume_1day": 0,
                "volume_1month": 0,
                "price_precision": 2,
                "data_start": "2023-01-01",
                "data_end": datetime.now().strftime("%Y-%m-%d")
            }
        ]
    
    def get_exchanges(self) -> List[Dict]:
        """Fetch available exchanges."""
        return self._make_request("exchanges")
    
    def get_symbols(self, exchange_id: str) -> List[Dict]:
        """Fetch symbols for a specific exchange."""
        return self._make_request(f"symbols?filter_symbol_id={exchange_id}_SPOT_BTC")

def filter_us_exchanges(exchanges: List[Dict]) -> List[str]:
    """Filter exchanges to include only US-friendly ones."""
    us_exchanges = ["COINBASE", "KRAKEN", "GEMINI"]
    return [ex["exchange_id"] for ex in exchanges if ex["exchange_id"] in us_exchanges]

def filter_btc_markets(symbols: List[Dict]) -> List[Dict]:
    """Filter symbols to include only BTC markets."""
    btc_markets = []
    seen_symbols = set()  # Track unique symbols
    
    for symbol in symbols:
        if "BTC" in symbol["asset_id_base"] or "BTC" in symbol["asset_id_quote"]:
            # Skip if we've already seen this symbol
            if symbol["symbol_id"] in seen_symbols:
                continue
                
            seen_symbols.add(symbol["symbol_id"])
            market_data = {
                "symbol": symbol["symbol_id"],
                "exchange": symbol["exchange_id"],
                "type": symbol["symbol_type"],
                "base_asset": symbol["asset_id_base"],
                "quote_asset": symbol["asset_id_quote"],
                "volume_1day": symbol.get("volume_1day", 0),
                "volume_1month": symbol.get("volume_1month", 0),
                "price_precision": symbol.get("price_precision", 0),
                "data_start": symbol.get("data_start", ""),
                "data_end": symbol.get("data_end", "")
            }
            btc_markets.append(market_data)
    
    return btc_markets

def main() -> None:
    """Main function to execute the BTC market analysis."""
    api_key = "204314b2-f25b-4111-b471-988a547c918c"
    client = CoinAPIClient(api_key)
    
    try:
        print("\nFetching exchange data...")
        exchanges = client.get_exchanges()
        us_exchanges = filter_us_exchanges(exchanges)
        print(f"Found {len(us_exchanges)} US exchanges")
        
        all_btc_markets = []
        seen_symbols = set()  # Track unique symbols across all exchanges
        
        for exchange in us_exchanges:
            print(f"\nFetching symbols for {exchange}...")
            symbols = client.get_symbols(exchange)
            btc_markets = filter_btc_markets(symbols)
            
            # Only add markets we haven't seen before
            for market in btc_markets:
                if market["symbol"] not in seen_symbols:
                    seen_symbols.add(market["symbol"])
                    all_btc_markets.append(market)
                    
            print(f"Found {len(btc_markets)} BTC markets on {exchange}")
        
        if not all_btc_markets:
            print("\nNo BTC markets found. Using fallback data...")
            for exchange in us_exchanges:
                symbols = client._get_fallback_symbols(exchange)
                btc_markets = filter_btc_markets(symbols)
                all_btc_markets.extend(btc_markets)
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(all_btc_markets)
        
        # Export to both CSV and JSON for flexibility
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export to CSV
        csv_filename = f"btc_markets_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\nData exported to {csv_filename}")
        
        # Export to JSON
        json_filename = f"btc_markets_{timestamp}.json"
        df.to_json(json_filename, orient="records", indent=2)
        print(f"Data exported to {json_filename}")
        
        print("\nNote: Some data may be from fallback sources due to API rate limits.")
        print("Consider running this script again after 24 hours for fresh data.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()