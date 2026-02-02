import httpx

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "YOUR_API_KEY"

async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            OPENWEATHER_URL,
            params={
                "q": city_name,
                "appid": API_KEY,
                "units": "metric",
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["main"]["temp"]
