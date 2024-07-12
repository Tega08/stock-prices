import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "EX6H0J322PQHY3MY"
NEWS_API_KEY = "API_KEY"
TWILIO_SID = "TWILIO_SID"
TWILIO_AUTH_TOKEN = "AUTH_TOKEN"

parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
response = requests.get(url=STOCK_ENDPOINT, params=parameter)
response.raise_for_status()
stock_prices = response.json()
print(stock_prices)
data = stock_prices["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

stock_diff = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if stock_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
stock_diff_percent = round((stock_diff/float(yesterday_closing_price)) * 100)
print(abs(stock_diff_percent))

if abs(stock_diff_percent) > 2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    first_three_articles = articles[:3]
    print(first_three_articles)

    formatted_articles = [(f"{COMPANY_NAME}: {up_down}{stock_diff_percent}%\nHeadline: {article['title']}. "
                           f"\nBrief: {article['description']}") for article in first_three_articles
                          ]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+12565877399',
            to='+2349156587463',
        )

        print(message.status)
