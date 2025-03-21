import requests
import os
import csv

FOLDER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "sensors")
)


def write_to_csv(data):
    CSV_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "output", "sensors2.csv")
    )
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    with open(CSV_PATH, mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=["id", "coordinates", "location", "date_installed"]
        )
        writer.writeheader()
        writer.writerows(data)


def fetch_data_from_urls(urls):
    """
    Fetch data from a list of URLs.

    Args:
        urls (list): List of URLs to fetch data from.

    Returns:
        dict: A dictionary with URLs as keys and their corresponding content or error messages as values.
    """
    sensor_data = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            data = response.json()

            sensor_info = {
                "id": data.get("id"),
                "coordinates": tuple(data.get("geometry", {}).get("coordinates", [])),
                "location": data.get("properties", {}).get("district"),
                "date_installed": data.get("properties", {}).get("Date_installed"),
            }
            sensor_data.append(sensor_info)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
    return sensor_data


if __name__ == "__main__":
    # Example list of URLs
    urls = [
        "https://bri3.fvh.io/opendata/r4c/24E124136E140271.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E140283.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E140287.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146069.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146080.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146083.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146087.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146118.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146126.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146128.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146155.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146157.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146167.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146186.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146190.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146198.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146218.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146224.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146235.geojson",
        "https://bri3.fvh.io/opendata/r4c/24E124136E146237.geojson",
    ]

    data = fetch_data_from_urls(urls)
    write_to_csv(data)
