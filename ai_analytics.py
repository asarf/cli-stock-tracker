import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.arima.model import ARIMA
from textblob import TextBlob
import yfinance as yf
from datetime import datetime, timedelta
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

def predict_next_day(ticker_symbol, days=1):
    """
    Predict the next day's price movement using Linear Regression
    Returns the predicted price and confidence score
    """
    try:
        # Get historical data for the past 30 days
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="60d")
        
        if hist.empty or len(hist) < 30:
            return None, None, "Insufficient data"
        
        # Prepare data
        df = hist.copy()
        df['PrevClose'] = df['Close'].shift(1)
        df['Return'] = (df['Close'] - df['PrevClose']) / df['PrevClose']
        df['Target'] = df['Return'].shift(-1)
        df = df.dropna()
        
        if len(df) < 20:
            return None, None, "Insufficient data after processing"
        
        # Features
        features = ['Open', 'High', 'Low', 'Close', 'Volume', 'Return']
        X = df[features].values
        y = df['Target'].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train model
        model = LinearRegression()
        model.fit(X_scaled, y)
        
        # Predict next day
        latest_data = X[-1].reshape(1, -1)
        latest_scaled = scaler.transform(latest_data)
        prediction = model.predict(latest_scaled)[0]
        
        # Calculate confidence (R² of the model)
        confidence = model.score(X_scaled, y)
        
        # Current price and predicted price
        current_price = df['Close'].iloc[-1]
        predicted_price = current_price * (1 + prediction)
        
        return predicted_price, confidence, None
    
    except Exception as e:
        return None, None, str(e)

def get_arima_forecast(ticker_symbol, days=5):
    """
    Use ARIMA model to forecast price trend for the next few days
    """
    try:
        # Get historical data
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="120d")
        
        if hist.empty or len(hist) < 60:
            return None, "Insufficient data"
        
        # Prepare data - use closing prices
        close_prices = hist['Close'].values
        
        # Fit ARIMA model - using a simple (5,1,0) model
        # In a production app, we would use auto_arima to find optimal parameters
        model = ARIMA(close_prices, order=(5, 1, 0))
        model_fit = model.fit()
        
        # Forecast
        forecast = model_fit.forecast(steps=days)
        
        # Calculate trend direction and strength
        current_price = close_prices[-1]
        forecast_end_price = forecast[-1]
        trend_pct = ((forecast_end_price - current_price) / current_price) * 100
        
        return trend_pct, None
    
    except Exception as e:
        return None, str(e)

def analyze_market_news(ticker_symbol):
    """
    Analyze recent news sentiment for a given ticker
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        
        if not news:
            return 0, 0, []
        
        # Get the 5 most recent news items
        recent_news = news[:5]
        
        sentiments = []
        headlines = []
        
        for item in recent_news:
            headline = item.get('title', '')
            if headline:
                analysis = TextBlob(headline)
                sentiment = analysis.sentiment.polarity
                sentiments.append(sentiment)
                headlines.append({
                    'headline': headline,
                    'sentiment': sentiment,
                    'date': datetime.fromtimestamp(item.get('providerPublishTime', 0))
                })
        
        if not sentiments:
            return 0, 0, []
        
        avg_sentiment = sum(sentiments) / len(sentiments)
        sentiment_strength = abs(avg_sentiment)
        
        return avg_sentiment, sentiment_strength, headlines
    
    except Exception as e:
        return 0, 0, []

def get_ai_insights(data):
    """
    Generate AI insights for each market index
    """
    insights = []
    
    for idx in data:
        country = idx["country"]
        index_name = idx["index_name"]
        ticker = idx.get("ticker", "")
        
        insight = {
            "country": country,
            "index_name": index_name,
            "current_value": idx["current_value"],
            "percentage_change": idx["percentage_change"],
        }
        
        # Price prediction
        if ticker:
            pred_price, confidence, error = predict_next_day(ticker)
            if pred_price is not None and confidence is not None:
                pred_change = ((pred_price - idx["current_value"]) / idx["current_value"]) * 100
                insight["prediction"] = {
                    "next_day_value": round(pred_price, 2),
                    "predicted_change": round(pred_change, 2),
                    "confidence": round(confidence * 100, 1)
                }
            
            # Trend analysis
            trend_pct, trend_error = get_arima_forecast(ticker)
            if trend_pct is not None:
                insight["trend"] = {
                    "direction": "up" if trend_pct > 0 else "down",
                    "strength": abs(trend_pct),
                    "forecast": round(trend_pct, 2)
                }
            
            # News sentiment
            sentiment, strength, headlines = analyze_market_news(ticker)
            if headlines:
                insight["sentiment"] = {
                    "score": round(sentiment, 2),
                    "strength": round(strength, 2),
                    "headlines": headlines[:2]  # Just include top 2 headlines
                }
        
        insights.append(insight)
    
    return insights

def format_prediction(prediction):
    """Format the prediction with color coding"""
    if not prediction:
        return "N/A"
    
    pred_change = prediction.get("predicted_change", 0)
    confidence = prediction.get("confidence", 0)
    
    if pred_change > 0:
        return f"{Fore.GREEN}+{pred_change}%{Style.RESET_ALL} (conf: {confidence}%)"
    else:
        return f"{Fore.RED}{pred_change}%{Style.RESET_ALL} (conf: {confidence}%)"

def format_trend(trend):
    """Format the trend forecast with color coding"""
    if not trend:
        return "N/A"
    
    forecast = trend.get("forecast", 0)
    
    if forecast > 1.5:
        return f"{Style.BRIGHT}{Fore.GREEN}Strong Uptrend{Style.RESET_ALL} ({forecast}%)"
    elif forecast > 0:
        return f"{Fore.GREEN}Slight Uptrend{Style.RESET_ALL} ({forecast}%)"
    elif forecast > -1.5:
        return f"{Fore.RED}Slight Downtrend{Style.RESET_ALL} ({forecast}%)"
    else:
        return f"{Style.BRIGHT}{Fore.RED}Strong Downtrend{Style.RESET_ALL} ({forecast}%)"

def format_sentiment(sentiment):
    """Format the sentiment with color coding"""
    if not sentiment:
        return "N/A"
    
    score = sentiment.get("score", 0)
    
    if score > 0.3:
        return f"{Style.BRIGHT}{Fore.GREEN}Very Positive{Style.RESET_ALL} ({score})"
    elif score > 0:
        return f"{Fore.GREEN}Positive{Style.RESET_ALL} ({score})"
    elif score > -0.3:
        return f"{Fore.RED}Negative{Style.RESET_ALL} ({score})"
    else:
        return f"{Style.BRIGHT}{Fore.RED}Very Negative{Style.RESET_ALL} ({score})"

def display_ai_insights(insights):
    """Display AI insights in a formatted table"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}AI MARKET INSIGHTS{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'Country':<10} {'Index':<20} {'Current':<10} {'Change':<10} {'Prediction':<25} {'Trend':<25} {'Sentiment':<20}{Style.RESET_ALL}")
    print("-" * 120)
    
    for insight in insights:
        country = insight["country"]
        index_name = insight["index_name"]
        current = insight["current_value"]
        change = insight["percentage_change"]
        
        # Format the change with color
        if change >= 0:
            change_str = f"{Fore.GREEN}+{change}%{Style.RESET_ALL}"
        else:
            change_str = f"{Fore.RED}{change}%{Style.RESET_ALL}"
        
        # Get prediction, trend and sentiment
        prediction = format_prediction(insight.get("prediction", {}))
        trend = format_trend(insight.get("trend", {}))
        sentiment = format_sentiment(insight.get("sentiment", {}))
        
        print(f"{country:<10} {index_name:<20} {current:<10} {change_str:<10} {prediction:<25} {trend:<25} {sentiment:<20}")
    
    print("-" * 120)
    print(f"{Fore.YELLOW}Note: Predictions are based on historical data and should not be used as financial advice.{Style.RESET_ALL}")

def generate_market_summary(insights):
    """Generate a natural language summary of market conditions"""
    if not insights:
        return "No market data available for analysis."
    
    # Count markets by direction
    up_markets = sum(1 for i in insights if i["percentage_change"] >= 0)
    down_markets = len(insights) - up_markets
    
    # Get strongest movements
    sorted_by_abs_change = sorted(insights, key=lambda x: abs(x["percentage_change"]), reverse=True)
    biggest_movers = sorted_by_abs_change[:3]
    
    # Get sentiment overview
    sentiments = [i.get("sentiment", {}).get("score", 0) for i in insights if "sentiment" in i]
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    
    # Generate summary
    summary = f"\n{Fore.CYAN}{Style.BRIGHT}MARKET SUMMARY:{Style.RESET_ALL}\n"
    
    # Overall market direction
    if up_markets > down_markets * 2:
        summary += f"{Fore.GREEN}Markets are broadly positive today with {up_markets} of {len(insights)} indices trading higher.{Style.RESET_ALL}\n"
    elif down_markets > up_markets * 2:
        summary += f"{Fore.RED}Markets are broadly negative today with {down_markets} of {len(insights)} indices trading lower.{Style.RESET_ALL}\n"
    else:
        summary += f"Markets are mixed today with {up_markets} indices up and {down_markets} down.\n"
    
    # Biggest movers
    summary += f"\n{Fore.YELLOW}Biggest movers:{Style.RESET_ALL}\n"
    for mover in biggest_movers:
        direction = "up" if mover["percentage_change"] >= 0 else "down"
        color = Fore.GREEN if direction == "up" else Fore.RED
        summary += f"- {mover['index_name']} ({mover['country']}): {color}{mover['percentage_change']}%{Style.RESET_ALL}\n"
    
    # Sentiment
    if sentiments:
        if avg_sentiment > 0.2:
            summary += f"\n{Fore.GREEN}News sentiment is generally positive across markets.{Style.RESET_ALL}\n"
        elif avg_sentiment < -0.2:
            summary += f"\n{Fore.RED}News sentiment is generally negative across markets.{Style.RESET_ALL}\n"
        else:
            summary += f"\nNews sentiment is neutral to mixed across markets.\n"
    
    # Predictions
    positive_predictions = sum(1 for i in insights if i.get("prediction", {}).get("predicted_change", 0) > 0)
    if positive_predictions > len(insights) * 0.7:
        summary += f"\n{Fore.GREEN}AI models predict positive movement for most markets tomorrow.{Style.RESET_ALL}\n"
    elif positive_predictions < len(insights) * 0.3:
        summary += f"\n{Fore.RED}AI models predict continued pressure on most markets tomorrow.{Style.RESET_ALL}\n"
    else:
        summary += f"\nAI models predict mixed market performance tomorrow.\n"
    
    return summary
