import os
import psycopg2
import csv
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
TABLE_NAME = "weather.sensors"  # Change this to your table name
GEOJSON_FOLDER = "./scripts/sensors"  # Change this to your GeoJSON folder path
# Establish connection to the database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Read all GeoJSON files in the folder and insert sensor data
for filename in os.listdir(GEOJSON_FOLDER):
    if filename.endswith(".geojson"):
        filepath = os.path.join(GEOJSON_FOLDER, filename)
        with open(filepath, encoding='utf-8') as geojson_file:
            data = json.load(geojson_file)
            
            # Ensure the data follows the expected structure
            if "type" in data and data["type"] == "Feature":
                properties = data["properties"]
                coordinates = data["geometry"]["coordinates"]
                
                # Extract relevant sensor data
                sensor_id = data.get("id")
                sensor_type = properties.get("Tyyppi")
                note = properties.get("Huomiot")
                attached = properties.get("Kiinnitystapa")
                install_date = properties.get("Asennettu_pvm")
                
                if sensor_id and coordinates:
                    # Check if the sensor ID already exists
                    cursor.execute(f"SELECT 1 FROM {TABLE_NAME} WHERE id = %s", (sensor_id,))
                    exists = cursor.fetchone()
                    
                    if not exists:
                        insert_sensor_query = f"""
                            INSERT INTO {TABLE_NAME} (id, location, type, note, attached, install_date)
                            VALUES (%s, POINT(%s, %s), %s, %s, %s, %s)
                        """
                        cursor.execute(insert_sensor_query, (sensor_id, coordinates[0], coordinates[1], sensor_type, note, attached, install_date))
            else:
                raise ValueError(f"Invalid GeoJSON format in {filename}: Expected a single Feature object.")

# Commit and close connection
conn.commit()
cursor.close()
conn.close()

print("GeoJSON data inserted successfully!")