import os
import psycopg2
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
TABLE_NAME = "weather.sensordata"  # Change this to your table name
CSV_FILE = "./scripts/makelankatu-2024.csv"  # Change this to your CSV file path

# Establish connection to the database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Read CSV and insert data
with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Read the first row as headers
    
    # Modify headers if one column needs to be renamed
    headers = ["sensor" if col == "dev-id" else col for col in headers]
    
    placeholders = ', '.join(['%s'] * len(headers))
    insert_query = f"INSERT INTO {TABLE_NAME} ({', '.join(headers)}) VALUES ({placeholders})"
    
    for row in reader:
        cursor.execute(insert_query, row)

# Commit and close connection
conn.commit()
cursor.close()
conn.close()

print("CSV data inserted successfully!")
