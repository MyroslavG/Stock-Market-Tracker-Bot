# Stock Market Tracker Bot 🤖

A real-time stock market monitoring bot that tracks key market indicators and provides technical analysis with buy/sell recommendations. The bot sends updates via Telegram, making it easy to stay informed about market movements.

## Quick Start 🚀

Want to use the bot without setting up your own? Simply:
1. Open Telegram
2. Search for `@stocktracker2025_bot`
3. Start the bot and follow the instructions

The bot will provide real-time market updates, technical analysis, and buy/sell recommendations for major indices and key tech stocks.

## Features 📊

- **Real-time Market Monitoring**
  - VIX Index tracking with panic alerts
  - Major indices (S&P 500, NASDAQ)
  - Key tech stocks (Tesla, NVIDIA)
  - Price and daily change tracking

- **Technical Analysis**
  - Moving Averages (20-day, 50-day)
  - MACD (Moving Average Convergence Divergence)
  - Volume Analysis
  - Trend Analysis

- **Smart Recommendations**
  - Buy/Sell/Hold signals
  - Confidence scoring
  - Multiple indicator confirmation
  - Real-time alerts

## Setup Guide (For Self-Hosting) 🛠️

If you want to run your own instance of the bot, follow these steps:

### Prerequisites

- Python 3.8 or higher
- Telegram account
- Telegram Bot Token (from BotFather)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-market-tracker-bot.git
cd stock-market-tracker-bot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your credentials:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Getting Your Telegram Bot Token

1. Open Telegram and search for "@BotFather"
2. Start a chat and send `/newbot`
3. Follow the instructions to create your bot
4. Copy the API token provided

### Getting Your Telegram Chat ID

1. Start a chat with your bot
2. Send any message to the bot
3. Visit: `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
4. Look for the "chat" object and find your "id"

## Usage 💻

1. Start the bot:
```bash
python main.py
```

2. The bot will:
   - Send a test message to confirm setup
   - Run an initial market check
   - Ask if you want to start continuous monitoring

3. For continuous monitoring:
   - Type 'y' when prompted
   - The bot will check the market every hour
   - You'll receive updates via Telegram

## Customization ⚙️

You can modify the following in `main.py`:

- `TICKERS` list to track different stocks
- Monitoring interval (default: 1 hour)
- Technical indicator parameters
- Alert thresholds

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer ⚠️

This bot is for informational purposes only. Always do your own research before making investment decisions. The bot's recommendations should not be considered as financial advice. 