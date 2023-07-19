from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from mausam_app.models import TotalForcast

city = ""


def saveforcaset(data):
    city = data
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=703bd8dc1cdf115091d4492540705cc8"
    r = requests.get(url.format(city)).json()
    now = datetime.now()
    print(requests.get(url.format(city)))
    print(now)
    current_time = datetime.now()
    ins = TotalForcast(
        time=current_time,
        city=r["name"],
        latitude=r["coord"]["lat"],
        longitude=r["coord"]["lon"],
        temperature=r["main"]["temp"],
        feels_like=r["main"]["feels_like"],
        temp_min=r["main"]["temp_min"],
        temp_max=r["main"]["temp_max"],
        pressure=r["main"]["pressure"],
        humidity=r["main"]["humidity"],
        visibility=r["visibility"],
        weather_description=r["weather"][0]["description"],
        weather_icon=r["weather"][0]["icon"],
    )
    ins.save()
    forecast_data = {
        'time': r['dt'],
        'city': r['name'],
        'latitude': r['coord']['lat'],
        'longitude': r['coord']['lon'],
        'temperature': r['main']['temp'],
        'feels_like': r['main']['feels_like'],
        'temp_min': r['main']['temp_min'],
        'temp_max': r['main']['temp_max'],
        'pressure': r['main']['pressure'],
        'humidity': r['main']['humidity'],
        'visibility': r['visibility'],
        'weather_description': r['weather'][0]['description'],
        'weather_icon': r['weather'][0]['icon'],
    }
    return forecast_data
def your_view(request):
    city = "Kolkata"
    dt = datetime.now()
    key = "703bd8dc1cdf115091d4492540705cc8"
    city = request.GET.get('city')
    option = request.GET.get('option')
    u = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid=703bd8dc1cdf115091d4492540705cc8"
    rres = requests.get(u.format(city)).json()
    city = rres[0]["name"]
    lat = rres[0]["lat"]
    lon = rres[0]["lon"]
    print(city, lat, lon)
    print(city)
    daily_ = weather_daily(lat, lon)
    hourly_ = weather_hourly(lat, lon)


    current_time = datetime.now()
    expiration_time = timedelta(minutes=10)
    time_threshold = current_time - expiration_time

    if TotalForcast.objects.filter(city=city, time__gte=time_threshold).exists():
        print("data taken from db")
        for forecast in TotalForcast.objects.filter(city=city):
            forecast_data = {
                'time': forecast.time,
                'city': forecast.city,
                'latitude': forecast.latitude,
                'longitude': forecast.longitude,
                'temperature': forecast.temperature,
                'feels_like': forecast.feels_like,
                'temp_min': forecast.temp_min,
                'temp_max': forecast.temp_max,
                'pressure': forecast.pressure,
                'humidity': forecast.humidity,
                'visibility': forecast.visibility,
                'weather_description': forecast.weather_description,
                'weather_icon': forecast.weather_icon,
            }

        combined_context = {'option': 'current', 'weather_data': forecast_data, 'weather_daily': daily_, 'weather_data_hour': hourly_ , "date":dt,"city":city}
        return render(request, 'index.html', combined_context)
    elif TotalForcast.objects.filter(city=city, time__lt=time_threshold).exists():
        deleted = TotalForcast.objects.filter(city=city, time__lt=time_threshold).delete()
        print(f"Deleted count: {deleted}")
        forecast_data = saveforcaset(city)
        print("data entered after deletion")

        combined_context = {'option': 'current', 'weather_data': forecast_data, 'weather_daily': daily_, 'weather_data_hour': hourly_, "date":dt,"city":city}
        return render(request, 'index.html', combined_context)
    else:
        forecast_data = saveforcaset(city)
        print("data has been written to the db (city not available)")

        combined_context = {'option': 'current', 'weather_data': forecast_data, 'weather_daily': daily_, 'weather_data_hour': hourly_, "date":dt,"city":city}
        return render(request, 'index.html', combined_context)

    forecast_data = saveforcaset(city)
    return render(request, 'index.html')



def weather_hourly(lat , lon):
    url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&cnt=48&appid=d503e785b497a75d198ce54c38e11af3".format(lat, lon)
    response = requests.get(url)
    weather_data_hour = response.json()
    if 'list' in weather_data_hour:
        return weather_data_hour['list']
    else:
        return None

def weather_daily(lat, lon):
    print(lat, lon)
    url ="https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&cnt=7&appid=d503e785b497a75d198ce54c38e11af3"
    print(url)
    response = requests.get(url.format(lat,lon))
    print(response)
    weather_list = response.json()
    if 'list' in weather_list:
        return weather_list['list']
    else:
        return None