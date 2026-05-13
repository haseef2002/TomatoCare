# src/utils/weather.py
import requests
import geocoder
from src.config.config import OPENWEATHER_API_KEY

def get_validated_weather(city_name=None):
    """
    Fetches live weather safely using IP geolocation or manual city input. 
    Never stores location data (Privacy/Legal Compliance).
    """
    try:
        # 1. Check if user provided a manual city
        if city_name and city_name.strip():
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name.strip()}&appid={OPENWEATHER_API_KEY}&units=metric"
        else:
            # 2. Track live location via IP if no city provided
            g = geocoder.ip('me')
            if not g.latlng: 
                return None
            lat, lon = g.latlng
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        
        # 3. Fetch weather with a strict timeout to prevent app hanging
        res = requests.get(url, timeout=5)
        res.raise_for_status() # Catches HTTP errors (like 404 City Not Found)
        data = res.json()
        
        # 4. Validate response
        if data.get("cod") != 200: 
            return None
        
        return {
            "city": data.get("name", city_name or "Local Field"),
            "temp": data["main"]["temp"],
            "hum": data["main"]["humidity"],
            "desc": data["weather"][0]["description"].title()
        }
    except requests.exceptions.RequestException as e:
        print(f"Weather API Network Error: {e}")
        return None
    except Exception as e:
        print(f"Weather System Error: {e}")
        return None # Graceful failure -> triggers manual sliders in the UI