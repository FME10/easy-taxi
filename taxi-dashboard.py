import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# OpenWeatherMap API-instellingen (gebruik je eigen API-sleutel)
OPENWEATHER_API_KEY = "your_openweather_api_key_here"

# Functie om weerdata op te halen voor een locatie
def get_weather_data(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
        }
    else:
        st.error("Weerdata kon niet worden opgehaald. Controleer je API-sleutel.")
        return None

# Streamlit-app
st.title("Taxi Demand Prediction Dashboard")
st.markdown(
    """
    **Overzicht:** Dit dashboard geeft inzicht in potentiële drukke locaties op basis van weerdata en evenementen.
    """
)

# Input: Stad of regio (voor demo starten we met Gent)
city = st.text_input("Voer de naam van een stad in:", "Gent")

# Haal weerdata op bij OpenWeatherMap
if city:
    weather_data = get_weather_data(city)
    if weather_data:
        st.subheader(f"Huidige weersinformatie voor {city}:")
        st.write(f"Temperatuur: {weather_data['temperature']}°C")
        st.write(f"Beschrijving: {weather_data['description']}")

        # Toon locatie op kaart
        st.subheader("Kaart van potentiële drukke locatie:")
        m = folium.Map(location=[weather_data["lat"], weather_data["lon"]], zoom_start=12)
        folium.Marker(
            [weather_data["lat"], weather_data["lon"]],
            popup=f"{city}: {weather_data['description']}, {weather_data['temperature']}°C",
            icon=folium.Icon(color="blue", icon="cloud"),
        ).add_to(m)
        folium_static(m)

# Toekomstige uitbreidingen:
# - Integreer Eventbrite API voor evenementenlocaties
# - Voeg historische data toe om drukte te voorspellen
# - Maak wekelijkse en maandelijkse planningen

st.info("Meer functionaliteiten worden toegevoegd in toekomstige versies.")
