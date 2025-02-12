# Project Verification Document

## Core Implementation
Key CoinAPI query implementation with rate limiting and fallback:

```python
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
```

## File References

### Source Code
- Repository: https://github.com/RudyTheThird/coinapi-btc-analysis
- Commit Hash: ce317f0 (Initial commit)

### Generated Files
SHA-256 Hashes for verification:

1. JSON Export (btc_markets_20250212_183635.json)
   - Hash: 88332E2001823881D48CDA6051D7C3AA751835881B3C18DEA1E0FA9687884789
   - Content: BTC market data in JSON format
   - URL: https://github.com/RudyTheThird/coinapi-btc-analysis/blob/main/btc_markets_20250212_183635.json

2. CSV Export (btc_markets_20250212_183635.csv)
   - Hash: 5126B606F25F44DB004EBF046BEA9E29E5B54F942914963492463FC9175E7EE4
   - Content: BTC market data in CSV format
   - URL: https://github.com/RudyTheThird/coinapi-btc-analysis/blob/main/btc_markets_20250212_183635.csv

3. Analysis Document (btc_market_analysis.md)
   - Hash: 5290BC8D61D111CE2D1416998C62945F2E7AE813353330ED57FDE606B0FCBD78
   - Content: Market analysis and findings
   - URL: https://github.com/RudyTheThird/coinapi-btc-analysis/blob/main/btc_market_analysis.md

## Verification Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/RudyTheThird/coinapi-btc-analysis
   cd coinapi-btc-analysis
   ```

2. Verify file hashes:
   ```powershell
   Get-FileHash -Algorithm SHA256 btc_markets_20250212_183635.json
   Get-FileHash -Algorithm SHA256 btc_markets_20250212_183635.csv
   Get-FileHash -Algorithm SHA256 btc_market_analysis.md
   ```

3. Check commit hash:
   ```bash
   git log --oneline
   ```

## Note
The JSON and CSV files contain the same data in different formats, generated from the CoinAPI response with fallback data due to rate limits. The analysis document provides insights based on this data.