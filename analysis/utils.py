import requests
import pandas as pd
import gzip
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

def fetch_geojson(url):
    """ Lataa ja käsittelee yksittäisen GeoJSON-tiedoston """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        geojson = response.json()
        return {
            'sensor_id': geojson['id'],
            'type': geojson['properties'].get('Tyyppi', 'Tuntematon'),
            'notes': geojson['properties'].get('Huomiot', '')
        }
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Virhe haettaessa GeoJSON-tiedostoa {url}: {e}")
        return None

def fetch_csv(url):
    """ Lataa ja lukee yksittäisen CSV-tiedoston """
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return pd.read_csv(gzip.open(BytesIO(response.content), 'rt'))
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Virhe haettaessa CSV-tiedostoa {url}: {e}")
        return None

def fetch_geojson_data(geojson_urls):
    """ Lataa kaiken GeoJSON-metadatan rinnakkain """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_geojson, geojson_urls))
    return pd.DataFrame([r for r in results if r])  # Poistetaan epäonnistuneet haut


def fetch_csv_data(csv_urls):
    """ Lataa kaikki CSV-tiedostot rinnakkain ja yhdistää ne """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_csv, csv_urls))
    return pd.concat([df for df in results if df is not None], ignore_index=True)
