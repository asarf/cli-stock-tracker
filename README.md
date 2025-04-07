# CLI Stock Market Tracker

A command-line application that provides real-time tracking of global stock market indices with automatic updates and customizable alerts.

## Features

- **Live Global Market Data**: Track 20 major indices from North America, Europe, Asia-Pacific, and South America
- **Real-time Updates**: Automatically refreshes data every minute
- **Customizable Alerts**: Set your own threshold for price change notifications
- **Clean Visualization**: View market data in a well-formatted table with visual indicators
- **AI-Powered Insights**: Get predictions, trend analysis, and sentiment analysis using machine learning
- **Market Summary**: Receive natural language summaries of market conditions

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd cli_stock_tracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application with default settings:
```
python main.py
```

Set a custom alert threshold (default is 5%):
```
python main.py --threshold 2.5
```

Enable AI-powered market insights and predictions:
```
python main.py --ai
```

Customize refresh interval (in minutes):
```
python main.py --interval 5 --ai
```

Combine multiple options:
```
python main.py --threshold 2.0 --interval 10 --ai
```

## Example Output

```
🚀 Starting Stock Market Tracker (refresh every 1 min, alert threshold: 5%)...
╒═════════╤═══════════════════╤═══════════════╤════════════╕
│ Country │ Index             │ Current Value │ % Change   │
╞═════════╪═══════════════════╪═══════════════╪════════════╡
│ USA     │ S&P 500           │ 5123.45       │ 0.75% 🔼   │
├─────────┼───────────────────┼───────────────┼────────────┤
│ JAPAN   │ Nikkei 225        │ 38765.23      │ -1.25% 🔽  │
├─────────┼───────────────────┼───────────────┼────────────┤
│ UK      │ FTSE 100          │ 7654.32       │ 0.32% 🔼   │
├─────────┼───────────────────┼───────────────┼────────────┤
│ GERMANY │ DAX               │ 18234.56      │ -0.45% 🔽  │
├─────────┼───────────────────┼───────────────┼────────────┤
│ FRANCE  │ CAC 40            │ 7543.21       │ 0.12% 🔼   │
├─────────┼───────────────────┼───────────────┼────────────┤
│ INDIA   │ NIFTY 50          │ 22345.67      │ 1.45% 🔼   │
├─────────┼───────────────────┼───────────────┼────────────┤
│ CHINA   │ Shanghai Composite│ 3245.67       │ -0.87% 🔽  │
╘═════════╧═══════════════════╧═══════════════╧════════════╛

🚨 ALERT: NIFTY 50 (INDIA) changed by 6.45%! (Threshold: 5%)
```

## How It Works

The application uses the following components:

- **main.py**: Entry point that sets up scheduling and handles command-line arguments
- **stock_fetcher.py**: Fetches stock data using the Yahoo Finance API
- **notifier.py**: Handles alerts when indices change beyond the threshold
- **utils.py**: Formats and displays data in a table format
- **ai_analytics.py**: Provides AI-powered market predictions and insights

## AI Features

When run with the `--ai` flag, the application provides several AI-powered features:

- **Price Predictions**: Uses machine learning to predict next-day price movements
- **Trend Analysis**: Employs ARIMA time series forecasting to predict market trends
- **Sentiment Analysis**: Analyzes recent news headlines to gauge market sentiment
- **Market Summary**: Generates natural language summaries of current market conditions
- **Visual Indicators**: Color-coded insights help quickly identify important information

## Dependencies

- yfinance: For fetching stock market data
- pandas: For data manipulation
- tabulate: For formatting data into tables
- APScheduler: For scheduling periodic data updates
- scikit-learn: For machine learning predictions
- statsmodels: For time series forecasting
- textblob: For sentiment analysis of news headlines
- colorama: For colored terminal output
- numpy: For numerical operations
- matplotlib: For data visualization (future features)

## Requirements

- Python 3.6 or higher
- Internet connection to fetch live market data

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
