import pandas as pd
import requests
import gzip
import matplotlib.pyplot as plt
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


def process_data(sensor_data, sensor_meta):
    """ Yhdistää datan ja metatiedot, laskee lämpötilaerot """
    sensor_data.rename(columns={'time': 'timestamp', 'dev-id': 'sensor_id'}, inplace=True)
    sensor_data['timestamp'] = pd.to_datetime(sensor_data['timestamp'])
    sensor_data['date'] = sensor_data['timestamp'].dt.date
    sensor_data = sensor_data.dropna(subset=["temperature"]) # Poistetaan puuttuvat lämpötilahavainnot
    sensor_data["temperature"] = pd.to_numeric(sensor_data["temperature"], errors='coerce')

    # Yhdistetään sensoridata ja metatiedot
    merged_data = pd.merge(sensor_data, sensor_meta, on='sensor_id', how='left')

    # Lasketaan päivittäinen keskilämpötila varjossa ja auringossa
    daily_avg = merged_data.groupby(["date", "type"])["temperature"].mean().unstack()
    daily_avg["Varjossa"] = daily_avg["Varjossa"].ffill()
    daily_avg["Auringossa"] = daily_avg["Auringossa"].ffill()
    daily_avg["ero"] = daily_avg["Auringossa"] - daily_avg["Varjossa"]

    return merged_data, daily_avg


def simulate_tree_removal(merged_data, daily_avg):
    """ 
    Simuloi puiden kaatamisen vaikutuksen lämpötilaan 
    - Sensoreille, jotka olivat varjossa ja sijaitsivat puussa, lisätään lämpötilaero (ero),
      koska ne muuttuisivat auringossa oleviksi sensoreiksi puiden kaatamisen jälkeen.
    """
    simuloitu_data = merged_data.copy()
    for date, row in daily_avg.iterrows():
        muutettavat = simuloitu_data[
            (simuloitu_data["date"] == date) &
            (simuloitu_data["type"] == "Varjossa") &
            (simuloitu_data["notes"].str.contains("Puussa", na=False))
        ]
        simuloitu_data.loc[muutettavat.index, "temperature"] += row["ero"]
    return simuloitu_data


def plot_results(daily_avg_before, daily_avg_after):
    """ Piirtää aikasarjakuvaajan lämpötilakehityksestä """
    plt.figure(figsize=(12, 6))
    plt.plot(daily_avg_before.index, daily_avg_before, label="Ennen puiden kaatamista", color="green")
    plt.plot(daily_avg_after.index, daily_avg_after, label="Puiden kaatamisen jälkeen", color="red", linestyle="dashed")
    plt.xlabel("Päivämäärä")
    plt.ylabel("Keskimääräinen lämpötila (°C)")
    plt.title("Päivittäinen lämpötilakehitys ennen ja jälkeen puiden kaatamisen")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()


# Pääohjelma
if __name__ == "__main__":

    # Sensorien ID:t
    SENSOR_IDS = [
        "24E124136E106616", "24E124136E106617", "24E124136E106618", "24E124136E106619",
        "24E124136E106635", "24E124136E106636", "24E124136E106637", "24E124136E106638",
        "24E124136E106643", "24E124136E106661", "24E124136E106674", "24E124136E106686"
    ]

    # Data-URL:t
    CSV_URLS = [f"https://bri3.fvh.io/opendata/makelankatu/makelankatu-{year}.csv.gz" for year in ["2024", "2025"]]
    GEOJSON_URLS = [f"https://bri3.fvh.io/opendata/makelankatu/{sensor_id}.geojson" for sensor_id in SENSOR_IDS]

    print("Haetaan sensorien metatiedot...")
    sensor_meta_df = fetch_geojson_data(GEOJSON_URLS)
    print("Haetaan lämpötiladataa...")
    sensor_data = fetch_csv_data(CSV_URLS)
    print("Käsitellään data...")
    merged_data, daily_avg = process_data(sensor_data, sensor_meta_df)
    print("Simuloidaan puiden kaataminen...")
    simuloitu_data = simulate_tree_removal(merged_data, daily_avg)

    # Lasketaan päivittäiset keskilämpötilat
    daily_avg_before = merged_data.groupby("date")["temperature"].mean()
    daily_avg_after = simuloitu_data.groupby("date")["temperature"].mean()

    print("Piirretään kuvaaja...")
    plot_results(daily_avg_before, daily_avg_after)
    print("Analyysi valmis!")
