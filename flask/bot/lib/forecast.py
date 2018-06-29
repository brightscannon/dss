import forecastio
FORECAST_TOKEN = "c259d4aeb593bc5e83d0c3f7ed916f5d" #나중엔 토큰 바꿔라
def forecast(lat=37.512, lng=126.954):
    forecast = forecastio.load_forecast(FORECAST_TOKEN, lat, lng)
    byHourly = forecast.hourly()
    return byHourly.summary

print(forecast())
