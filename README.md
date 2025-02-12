# CoinAPI BTC Market Analysis

Task ID: 2025-02-12_23:13__RT28

A Python script that analyzes BTC markets on US-friendly cryptocurrency exchanges using the CoinAPI.io API.

## Features

- Queries CoinAPI.io for BTC market data
- Focuses on US-friendly exchanges (Coinbase, Kraken, Gemini)
- Handles API rate limits with graceful fallback
- Prevents duplicate entries
- Exports data in both JSON and CSV formats
- Includes detailed market analysis

## Requirements

- Python 3.6+
- Required packages:
  * requests
  * pandas

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd coinapi-btc-analysis
```

2. Install required packages:
```bash
pip install requests pandas
```

3. Set up your CoinAPI key:
   - Get your API key from [CoinAPI.io](https://www.coinapi.io/)
   - Replace the `api_key` variable in `main.py` with your key

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Fetch exchange and market data from CoinAPI
2. Filter for US exchanges and BTC markets
3. Export results to:
   - `btc_markets_[timestamp].json`
   - `btc_markets_[timestamp].csv`
4. Generate market analysis in `btc_market_analysis.md`

## Output Files

- `main.py`: Main script file
- `btc_markets_[timestamp].json`: Market data in JSON format
- `btc_markets_[timestamp].csv`: Market data in CSV format
- `btc_market_analysis.md`: Detailed market analysis
- `README.md`: This documentation file

## Rate Limiting

The script implements a conservative rate limiting approach:
- 10-second delay between requests
- Fallback to basic market data when rate limits are hit
- Detailed logging of API responses

## Analysis

The market analysis includes:
- Market structure overview
- Exchange coverage
- Trading pair distribution
- Risk considerations
- Trading implications

## License

MIT License

## Disclaimer

This tool is for informational purposes only. Always verify market data from multiple sources before making trading decisions.
