# Global Market Pulse: AI-Powered Stock Tracker

A command-line application that provides real-time tracking of 20 global stock market indices with AI-powered insights, trend analysis, and interactive settings management.

## Features

- **Live Global Market Data**: Track 20 major indices from North America, Europe, Asia-Pacific, and South America
- **Real-time Updates**: Automatically refreshes data at customizable intervals
- **Customizable Alerts**: Set your own threshold for price change notifications
- **Clean Visualization**: View market data in a well-formatted table with visual indicators
- **AI-Powered Insights**: Get predictions, trend analysis, and sentiment analysis using machine learning
- **Market Summary**: Receive natural language summaries of market conditions
- **Interactive Settings**: Change configuration options on-the-fly without restarting the application
- **Color-Coded Interface**: Quickly identify important information with color highlighting

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

### Command Line Options

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

### Interactive Settings Menu

While the application is running:
1. Press `m` at any time to open the settings menu
2. Use the menu to:
   - Change alert threshold
   - Adjust refresh interval
   - Toggle AI insights on/off
   - Return to market view
   - Exit application

All changes take effect immediately without needing to restart the application.

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
- **settings_menu.py**: Manages interactive settings and user preferences

## AI Features

The application provides several AI-powered features:

- **Price Predictions**: Uses machine learning (Linear Regression) to predict next-day price movements with confidence scores
- **Trend Analysis**: Employs ARIMA time series forecasting to predict market trends over the next few days
- **Sentiment Analysis**: Analyzes recent news headlines using TextBlob to gauge market sentiment
- **Market Summary**: Generates natural language summaries of current market conditions
- **Visual Indicators**: Color-coded insights help quickly identify important information

### AI Implementation Details

- **Machine Learning**: Uses scikit-learn for price prediction models
- **Time Series Analysis**: Implements statsmodels ARIMA for trend forecasting
- **Natural Language Processing**: Leverages TextBlob for sentiment analysis of news
- **Data Processing**: Employs pandas and numpy for efficient data manipulation
- **Visualization**: Uses colorama for terminal-based color highlighting

## Dependencies

- **Data Acquisition**:
  - yfinance: For fetching stock market data
  - pandas: For data manipulation

- **Visualization**:
  - tabulate: For formatting data into tables
  - colorama: For colored terminal output

- **System Components**:
  - APScheduler: For scheduling periodic data updates
  - numpy: For numerical operations

- **AI and Machine Learning**:
  - scikit-learn: For machine learning predictions
  - statsmodels: For time series forecasting
  - textblob: For sentiment analysis of news headlines
  - matplotlib: For data visualization (future features)

## Requirements

- Python 3.6 or higher
- Internet connection to fetch live market data
- Terminal that supports ANSI color codes (most modern terminals)

## License

MIT

## Contributing

Contributions are welcome! Here are some ways you can contribute:

- Add support for more markets and indices
- Improve AI prediction accuracy
- Enhance the user interface
- Add new features like portfolio tracking
- Fix bugs and improve performance

Please feel free to submit a Pull Request or open an Issue to discuss potential improvements.
