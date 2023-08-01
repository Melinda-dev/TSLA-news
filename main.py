import requests
import os
from twilio.rest import Client
from api_key import *
from twilio.http.http_client import TwilioHttpClient

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

def get_news():

    news_parameter = {
        "apiKey": news_api_key,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameter)
    news_response.raise_for_status()
    articles = news_response.json()["articles"][:3]
    print(news_response.raise_for_status())
    print(articles)
    return articles

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


def get_stock_data():

    TIME_SERIES_DAILY = "TIME_SERIES_DAILY"

    stock_parameter = {
        "function": TIME_SERIES_DAILY,
        "symbol": STOCK,
        "apikey": stock_api_key,
    }
    stock_response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameter)
    stock_response.raise_for_status()
    stock_data = stock_response.json()
    print(stock_response.raise_for_status())
    return stock_data


def send_SMS():

    client = Client(twilio_account_sid, twilio_auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+14705169436',
            to='+61470557910',
        )



stock_price = get_stock_data()
stock_price_list = []
for date in stock_price['Time Series (Daily)']:
    # print(date)
    stock_price_list.append(stock_price['Time Series (Daily)'][date]['4. close'])
print(stock_price_list)
# print(type(stock_price_list[0]))
difference = (float(stock_price_list[0]) - float(stock_price_list[1])) /float(stock_price_list[1])
print(difference)

if difference > 0:
    up_down = "↑"
else:
    up_down = "↓"

if abs(difference) >= 0.0000000000000000000005:
    result = get_news()
    formatted_articles = []
    for article in result:
        formatted_articles.append(f"{STOCK}: {up_down}{difference}*100%\nHeadline: {article['title']}. \nBrief: {article['description']}")
    send_SMS()









## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

