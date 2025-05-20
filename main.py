import datetime
import os
import time

import requests
import yfinance as yf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print(
        "Error: Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables"
    )
    print("You can create a .env file with these variables:")
    print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
    print("TELEGRAM_CHAT_ID=your_chat_id_here")
    exit(1)

TICKERS = ["^VIX", "SPY", "QQQ", "TSLA", "NVDA"]


def notify_telegram(message):
    print(f"[{datetime.datetime.now()}] Sending notification...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")


def analyze_ticker(ticker):
    try:
        # Get historical data for calculations
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if df is None or df.empty:
            print(f"No data available for {ticker}")
            return None

        # Get the latest values and convert to float
        latest = df.iloc[-1]
        close = float(latest["Close"])
        volume = float(latest["Volume"])

        # Calculate daily change
        prev_close = float(df.iloc[-2]["Close"])
        daily_change = ((close - prev_close) / prev_close) * 100

        # Format the message
        if ticker == "^VIX":
            message = f"📊 *VIX Index*\n"
            message += f"Current: {close:.2f}\n"
            message += f"Change: {daily_change:+.2f}%\n"

            # Add VIX alert
            if close > 30:
                message += "\n🧨 *PANIC ALERT:* VIX is above 30. Buying opportunity setting up."
        else:
            # Calculate technical indicators for stocks
            # Moving Averages
            df["MA20"] = df["Close"].rolling(window=20).mean()
            df["MA50"] = df["Close"].rolling(window=50).mean()
            ma20 = float(df["MA20"].iloc[-1])
            ma50 = float(df["MA50"].iloc[-1])

            # MACD
            exp1 = df["Close"].ewm(span=12, adjust=False).mean()
            exp2 = df["Close"].ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            macd_value = float(macd.iloc[-1])
            signal_value = float(signal.iloc[-1])

            # Volume Analysis
            avg_volume = float(df["Volume"].rolling(window=20).mean().iloc[-1])
            volume_ratio = volume / avg_volume if avg_volume > 0 else 1

            message = f"📈 *{ticker}*\n"
            message += f"Price: ${close:.2f}\n"
            message += f"Change: {daily_change:+.2f}%\n"
            message += f"Volume: {volume:,.0f} ({volume_ratio:.1f}x avg)\n\n"

            message += f"📊 *Technical Indicators:*\n"
            message += f"MA20: ${ma20:.2f}\n"
            message += f"MA50: ${ma50:.2f}\n"
            message += f"MACD: {macd_value:.2f}\n"
            message += f"Signal: {signal_value:.2f}\n"

            # Add alerts and evaluate buy/sell signals
            alerts = []
            buy_signals = 0
            sell_signals = 0

            # Moving Average Analysis
            if close < ma20:
                alerts.append(f"⚠️ Price below 20-day MA (${ma20:.2f})")
                sell_signals += 1
            elif close > ma20:
                alerts.append(f"✅ Price above 20-day MA (${ma20:.2f})")
                buy_signals += 1

            if close < ma50:
                alerts.append(f"⚠️ Price below 50-day MA (${ma50:.2f})")
                sell_signals += 1
            elif close > ma50:
                alerts.append(f"✅ Price above 50-day MA (${ma50:.2f})")
                buy_signals += 1

            # MACD Analysis
            if macd_value > signal_value:
                alerts.append("📈 MACD above signal line (Bullish)")
                buy_signals += 1
            else:
                alerts.append("📉 MACD below signal line (Bearish)")
                sell_signals += 1

            # Volume Analysis
            if volume_ratio > 2:
                alerts.append(f"🔥 High volume: {volume_ratio:.1f}x average")
                if daily_change > 0:
                    buy_signals += 1
                else:
                    sell_signals += 1

            # Trend Analysis
            if ma20 > ma50:
                alerts.append("📈 Uptrend: MA20 above MA50")
                buy_signals += 1
            else:
                alerts.append("📉 Downtrend: MA20 below MA50")
                sell_signals += 1

            # Add alerts to message
            if alerts:
                message += "\n🔔 *Alerts:*\n" + "\n".join(alerts)

            # Add buy/sell recommendation
            message += "\n🎯 *Recommendation:*\n"
            if buy_signals > sell_signals:
                strength = (buy_signals / (buy_signals + sell_signals)) * 100
                message += f"BUY ({strength:.0f}% confidence)\n"
                message += (
                    f"• {buy_signals} bullish signals vs {sell_signals} bearish signals"
                )
            elif sell_signals > buy_signals:
                strength = (sell_signals / (buy_signals + sell_signals)) * 100
                message += f"SELL ({strength:.0f}% confidence)\n"
                message += (
                    f"• {sell_signals} bearish signals vs {buy_signals} bullish signals"
                )
            else:
                message += "HOLD (Neutral)\n"
                message += (
                    f"• Equal number of bullish and bearish signals ({buy_signals})"
                )

        return message
    except Exception as e:
        print(f"Error analyzing {ticker}: {str(e)}")
        return None


def run_checker():
    summary = []
    for ticker in TICKERS:
        try:
            message = analyze_ticker(ticker)
            if message:
                summary.append(message)
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")

    if summary:
        notify_telegram("\n\n" + "=" * 30 + "\n\n".join(summary))
    else:
        print(f"[{datetime.datetime.now()}] No data available.")


def test_telegram():
    print("Testing Telegram connection...")
    test_message = (
        "🤖 *Stock Tracker Bot Test*\n\nBot is now active and monitoring:\n"
        + "\n".join([f"• {ticker}" for ticker in TICKERS])
    )
    notify_telegram(test_message)
    print("Test message sent! Check your Telegram.")


if __name__ == "__main__":
    # Test the bot first
    test_telegram()

    # Run a single check
    print("Running initial stock check...")
    run_checker()

    # Ask user if they want to continue monitoring
    response = input("\nDo you want to start continuous monitoring? (y/n): ")
    if response.lower() == "y":
        print("Starting continuous monitoring...")
        while True:
            run_checker()
            time.sleep(3600)
    else:
        print("Exiting...")
