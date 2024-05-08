import requests

def fetch_weather(latitude, longitude):
    #Url полученный с сайта open meteo с предварительно заготовленными необходимыми параметрами.
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,rain,snowfall,surface_pressure,wind_speed_10m,wind_direction_10m&forecast_days=1"
    response = requests.get(url)
    #Статус 200- успешно
    if response.status_code == 200:
        #Выбираем необходимые нам элементы из объекта json полученного по api
        data = response.json()
        weather_data = {
            "timestamp": data["current"]["time"],
            "temperature": data["current"]["temperature_2m"],
            "wind_speed": get_m_s(data["current"]["wind_speed_10m"]),
            "wind_direction": get_wind_direction(data["current"]["wind_direction_10m"]),
            "pressure": data["current"]["surface_pressure"],
            "rain": data["current"]["rain"],
            "snowfall": data["current"]["snowfall"]
        }
        return weather_data
    else:
        print("Failed to fetch weather data")
        return None
#Делим окружность компаса на 16 равных частей для формирования обозначений направления ветра
def get_wind_direction(degrees):
    directions = ["С", "ССВ", "СВ", "ВСВ", "В", "ВЮВ", "ЮВ", "ЮЮВ", "Ю", "ЮЮЗ", "ЮЗ", "ЗЮЗ", "З", "ЗСЗ", "СЗ", "ССЗ"]
    index = round(degrees / 22.5) % 16
    return directions[index]
#Переводим км/ч в м/с
def get_m_s(value):
    value=(value*1000)/3600
    return value