# Algorithimic-Auto-Trade-Bot

The Algorithmic Auto Trade Bot is a web application designed to analyze stock market data and sentiment analysis of financial news to generate trading signals. It uses historical price data from the Yahoo Finance API and performs technical analysis to identify potential buy and sell opportunities. The bot also incorporates sentiment analysis on financial news articles to gauge market sentiment and adjust trading decisions accordingly. Overall, this is an automated trading algorithim integrating sentimentality analysis from financial news, technical metrics, and risk-mitigating strategies. 

## Features 

The Algorithmic Auto Trade Bot utilizes the following features:

* Momentum Trading: The bot identifies stocks with upward momentum and potential for continued price increases. The final algorithim is
  built with a base momentum trading algorithim. 
* Moving Average: The bot calculates and analyzes moving averages for different technical metrics to identify trends and potential
  entry/exit points.
* Sentimental Analysis: The bot performs sentiment analysis on financial news articles to understand market sentiment and adjust trading       decisions. By webscraping financial news from any given day, the bot reads and estiamtes an NLTK severity rating. If any news article        suggests an idea that is extreme enough to shift market prices one way or another, bot buys/sells correspondingly.
* Bollinger Bands: The bot calculates Bollinger Bands to identify potential overbought and oversold conditions. This provides a measure of
  when the market typically indicates a shift or has potential breakout signals.
* MACD (Moving Average Convergence-Divergence): The bot calculates MACD using TA-lib to identify bullish and bearish crossovers for trading    signals. This helps indicate trend reversals and gauge the strength of a trend. Utilizing this in combination with Bollinger Bands helps     identify buy/sell points.
* Risk Management (Position Sizing): The bot employs a risk management strategy to determine the appropriate position size based on risk       percentage. Given a certain capital, we allocate a certain percentage to invest per trade. This helps limit potential losses and manage      overall portfolio risk.


## Future Implementations

The Algorithmic Auto Trade Bot has the following potential future features:

* Integration with additional technical indicators: The bot can be enhanced by incorporating additional technical indicators to generate       more accurate trading signals. By involving more risk strategies such as trailing stop-loss and technical metrics like RSI, trading          algorithim will be more reliable in drastic shifts.
* Machine learning algorithms: Utilizing machine learning algorithms could enhance the bot's ability to learn from historical data and adapt    to changing market conditions. In addition to manual technical/sentimental analysis, an ML appraoch could aid the model.
* Portfolio management: Adding portfolio management features, such as tracking multiple stocks and optimizing portfolio allocations, can       further enhance the bot's capabilities.

## Installation

To get started with the Algorithmic Auto Trade Bot, follow these steps:

1. Clone this repository: git clone https://github.com/vishalramvelu/Algorithimic-Auto-Trade-Bot.git
2. Install the required dependencies: pip install -r requirements.txt
3. Customize the trading parameters:
   * Set the start_date and end_date variables to define the date range for the analysis
   * Modify the tickers list to include the desired stock tickers.
4. Run the Flask application to start the web server.
5. Access the application in your web browser using the provided URL.
6. Review the output, including price charts, technical indicators, and trading signals.

## Usage 

Once the Flask application is running, you can access the Algorithmic Auto Trade Bot through your web browser. The application provides a user interface where you can customize the trading parameters, view price charts, technical indicators, and trading signals for the selected stocks. From this information, you can selectively choose the relevant data and metrics for buying/selling to make informed decisions. 

## Credits 

This project was developed by Vishal Ramvelu. Contributions are welcome via pull requests. For any questions or suggestions, please contact rv.vishal@gmail.com.

## License 

This project is licensed under the MIT License.
  
