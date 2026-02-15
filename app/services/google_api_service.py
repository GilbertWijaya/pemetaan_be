import requests
from urllib.parse import urlencode
from app.config import Config

class GoogleApiService:

    @staticmethod
    def get_all_places(prompt: str) -> dict:
        if not prompt:
            raise ValueError("Prompt is required")

        base_url = Config.GOOGLE_API_ALL_QUERY
        api_key = Config.GOOGLE_API_KEY

        if not base_url or not api_key:
            raise RuntimeError("Google API configuration missing")

        params = {
            "query": prompt,
            "key": api_key
        }

        url = f"{base_url}?{urlencode(params)}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise RuntimeError("Failed to fetch data from Google API")

            return response.json()

        except requests.RequestException as e:
            raise RuntimeError(f"Google API request failed: {str(e)}")
    
    @staticmethod
    def get_detail_place(place_id: str, fields: list[str] = None) -> dict:
        if not place_id:
            raise ValueError("place_id is required")

        base_url = Config.GOOGLE_API_DETAIL_QUERY
        api_key = Config.GOOGLE_API_KEY

        if not base_url or not api_key:
            raise RuntimeError("Google API configuration missing")

        # Default fields jika tidak diberikan
        if not fields:
            fields = ["formatted_phone_number", "website"]

        params = {
            "place_id": place_id,
            "fields": ",".join(fields),
            "key": api_key
        }

        url = f"{base_url}?{urlencode(params)}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise RuntimeError("Failed to fetch place details")

            return response.json()

        except requests.RequestException as e:
            raise RuntimeError(f"Google Detail API request failed: {str(e)}")
