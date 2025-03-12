import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def get_weather(api_key, city):
    # Önce şehrin place_id'sini bul
    place_url = "https://www.meteosource.com/api/v1/free/find_places"
    place_params = {
        "text": city,
        "language": "en",
        "key": api_key
    }
    
    try:
        place_response = requests.get(place_url, params=place_params)
        place_response.raise_for_status()
        places = place_response.json()
        
        if not places:
            print("Şehir bulunamadı.")
            return
        
        place_id = places[0]['place_id']
        
        # Hava durumu verilerini al
        weather_url = f"https://www.meteosource.com/api/v1/free/point?place_id={place_id}&sections=current&key={api_key}"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data.get('current', {})
        print(f"{city} için hava durumu:")
        print(f"Sıcaklık: {current.get('temperature', 'Bilgi yok')}°C")
        print(f"Durum: {current.get('summary', 'Bilgi yok')}")
        print(f"Yağış: {current.get('precipitation', {}).get('total', 'Bilgi yok')} mm")
        
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
    return current

def generate_outfit(gemini_api_key, weather_data):

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")
        
        prompt = f"""Aşağıdaki hava durumu koşullarına uygun giyim önerileri yap:
        - Sıcaklık: {weather_data.get('temperature', 'Bilinmiyor')}°C
        - Hava Durumu: {weather_data.get('summary', 'Bilinmiyor')}
        - Yağış: {weather_data.get('precipitation', {}).get('total', 0)} mm
        - Rüzgar Hızı: {weather_data.get('wind', {}).get('speed', 0)} m/s
        
        Günlük aktiviteler için pratik ve stil sahibi 3 farklı kombin öner. Kısa ve maddeler halinde ver."""
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# Kullanım örneği
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Meteosource'dan alacağınız ücretsiz API anahtarı
CITY = input("Hava durumu için şehir adı girin: ")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Google Gemini'den alacağınız API anahtarı

result = get_weather(WEATHER_API_KEY, CITY)
suggestion = generate_outfit(GEMINI_API_KEY, result)
print(suggestion)