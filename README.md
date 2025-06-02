# Algorithimic Auto Trade Bot

This is an automated momentum trading algorithim integrating sentimentality analysis from financial news, technical metrics, and risk-mitigating strategies. It uses historical price data from the Yahoo Finance API and performs technical analysis to identify potential buy and sell opportunities. The bot also incorporates sentiment analysis on financial news articles to gauge market sentiment and adjust trading decisions accordingly.  

## Framework 

## Features 
* Momentum Trading: Identifies stocks with upward momentum and potential for continued price increases
* Sentimental Analysis: Performs sentiment analysis on financial news articles to understand market sentiment and adjust trading decisions daily
* Bollinger Bands + Moving Averge Convergence-Divergence: Used to identify potential bullish and bearish conditions for trading signals using TA-lib
* Risk Management (Position Sizing): Determines the appropriate position size based on risk percentage managing profit/loss ratio

## Build
To get started with the Algorithmic Auto Trade Bot, follow these steps:

1. Clone this repository: `git clone https://github.com/vishalramvelu/Algorithimic-Auto-Trade-Bot.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Customize the trading parameters:
   * Set the start_date and end_date variables to define the date range for the analysis
   * Modify the tickers list to include the desired stock tickers.
4. Run Flask application to start web server: `python3 app.py`
5. Review the output, including price charts, technical indicators, and trading signals.

## Contributing
Contributions are welcome! If you'd like to enhance this project or report issues, please submit a pull request or open an issue.

  
