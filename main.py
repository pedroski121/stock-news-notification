from calendar import weekday
import requests
import datetime as dt
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCKPRICE_API_KEY = "STOCKPRICE_API_KEY FROM https://www.alphavantage.co"
NEWS_API_KEY = "NEWS_API_KEY FROM https://newsapi.org/v2/everything"

# Twilio
TWILIO_SID = "TWILIO_SID FROM https://www.twilio.com"
AUTH_TOKEN = "AUTH_TOKEN FROM https://www.twilio.com"
API_KEY = 'API_KEY GOES HERE FROM https://www.twilio.com'


STOCKPRICE_URL = 'https://www.alphavantage.co/query'
NEWS_URL = 'https://newsapi.org/v2/everything'

def get_news():
    news_data = requests.get(NEWS_URL, params=newsurl_parameters)
    news_data.raise_for_status()
    articles = news_data.json()['articles']
    first_three = []
    for article in range(0, 3):
        first_three.append(articles[article])
    return first_three


stockprice_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCKPRICE_API_KEY
}
newsurl_parameters = {"q": COMPANY_NAME,
                      "sortBy": 'popularity', "apikey": NEWS_API_KEY}


data = requests.get(STOCKPRICE_URL, params=stockprice_parameters)
data.raise_for_status()
stock_prices = data.json()["Time Series (Daily)"]
stock_data = [value for key, value in stock_prices.items()]

yesterday_data = stock_data[0]
yesterday_closing_price = float(yesterday_data['4. close'])

day_bfr_yesterday = stock_data[1]
day_bfr_yesterday_closing_price = float(day_bfr_yesterday['4. close'])


diff_bw_prices = yesterday_closing_price - day_bfr_yesterday_closing_price
diff = int((diff_bw_prices/yesterday_closing_price * 100))
perc_diff = abs(diff)

news_summary_list = []
if perc_diff >= 5:
    news_list = get_news()
    for news in news_list:
        headline = f"{news['title']}"
        headline_ = headline.find('-')
        new_headline = f"{headline[:headline_] } TSLA"
        brief = news['content']
        brief_ = brief.find('-')
        brief_data = brief.split('[')
        brief_news = brief_data[0][brief_ + 1:]
        news = f"""
            {STOCK}:{"🔺" if diff > 0 else "🔻" } {perc_diff}%
            Headline:{headline}
            Brief: {brief_news}
        """
        news_summary_list.append(news)
    message = """""".join(n for n in news_summary_list)
    client = Client(TWILIO_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
            body=message.strip(),  # message won't be received if not strip
            from_='PHONE NUMBER',
            to='PHONE NUMBER'
        )
    print(message.status)
