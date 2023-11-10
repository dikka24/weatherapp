from django.shortcuts import render
import json 
import urllib.request
from urllib.parse import quote
from urllib.error import HTTPError

def index(request):
    error_message = ""  # Инициализация переменной ошибки
    data = {}           # Инициализация переменной данных

    if request.method == 'POST':
        city = request.POST['city']
        try:
            res = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid=bd964f4db4905165f3118cd245c240bd').read()
            json_data = json.loads(res)
            data = {
                'country_code': str(json_data['sys']['country']),
                'coordinate': str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
                'temp': str(round(float(json_data['main']['temp']) - 273.15, 1)) + '°C',
                'feels_like': str(round(float(json_data['main']['feels_like']) - 273.15, 1)) + '°C',
                'pressure': str(json_data['main']['pressure']),
                'humidity': str(json_data['main']['humidity']),
            }
        except HTTPError as e:
            if e.code == 404:
                error_message = "Город не найден."
            else:
                error_message = f"HTTP Error: {e.code}"
        except urllib.error.URLError as e:
            error_message = f"URL Error: {e.reason}"
        except json.JSONDecodeError as e:
            error_message = f"JSON Decode Error: {e}"

    return render(request, 'index.html', {'city': city, 'data': data, 'error_message': error_message})

