import requests
import os
from twilio.rest import Client

api_key = os.environ.get("OWM_API_KEY")  # Weather API key
account_sid = os.environ.get("TW_ACCOUNT_SID")
auth_token = os.environ.get("TW_AUTH_TOKEN")

parameters = {
    "lat": 52.921940,
    "lon": 12.794090,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
data = response.json()
weather = data["hourly"][0]["weather"][0]["id"]
slice_object = slice(12)
weather_data = data["hourly"][slice_object]
condition_codes = []

for hour_data in weather_data:
    code = hour_data["weather"][0]["id"]
    condition_codes.append(code)

will_it_rain = False

for n in condition_codes:
    if n < 700:
        will_it_rain = True


from_number = os.environ.get("F_NUM")
to_number = os.environ.get("T_NUM")
if will_it_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="It is going to rain today. Remember to bring an ☂️.",
            from_=from_number,
            to=to_number,
        )

    print(message.status)
