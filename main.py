import requests
from twilio.rest import Client

account_sid = "YOUR TWILIO SID"
auth_token = "YOUR TWILIO TOKEN"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"



parameters_stats = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "outputsize":"compact",
    "apikey":"YOUR STOCK API KEY",
}

r = requests.get(url="https://www.alphavantage.co/query", params=parameters_stats)
data = r.json()
date_list = []
for x in data["Time Series (Daily)"]:
    date_list.append(x)

open_price = float(data["Time Series (Daily)"][date_list[0]]["4. close"])
closing_price = float(data["Time Series (Daily)"][date_list[1]]["4. close"])


diff = closing_price-open_price
percent = round(diff/closing_price*100, 2)




parameters_news = {
    "apiKey": "YOUR NEWS API KEY",
    "language": "en",
    "q": COMPANY_NAME,
    "sortBy": "relevancy"
}

r = requests.get(url="https://newsapi.org/v2/everything?", params=parameters_news)
data = r.json()
news_text = ""
for x in range(0,3):
    title = data["articles"][x]["title"]
    description = data["articles"][x]["description"]
    news_text += f"Headline: {title}\n"
    news_text += f"Brief: {description}\n"



if percent > 0:
    msg_text = f"TSLA: 🔺{percent}%\n{news_text}"
else:
    msg_text = f"TSLA: 🔻{percent}%\n{news_text}"

print(msg_text)
client = Client(account_sid, auth_token)

message = client.messages \
            .create(
                body=msg_text,
                from_='YOUR TWILLIO PHONE NUMBER',
                to='YOUR PHONE NUMBER'
            )
print(message.status)


