import requests
import psycopg2
import sys

# Usage:
#   python extract_load.py 2026-09-01
#   python extract_load.py 2026-09-01 2026-09-10

if len(sys.argv) == 2:
    start_date = end_date = sys.argv[1]
elif len(sys.argv) == 3:
    start_date, end_date = sys.argv[1], sys.argv[2]
else:
    print("Usage: python extract_load.py <start_date> [end_date]")
    sys.exit(1)

# Fetch weather data from Open-Meteo API
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 12.9716,   # Bangalore
    "longitude": 77.5946,
    "start_date": '2026-08-12', #start_date,
    "end_date": '2026-09-12',  #end_date,
    "daily": ["temperature_2m_max", "precipitation_sum"],
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params)
data = response.json()

# Connect to Postgres (container service name from docker-compose)
conn = psycopg2.connect(
    dbname="warehouse",
    user="de",
    password="de",
    host="postgres",
    port="5432"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS raw_weather (
    city TEXT,
    date DATE,
    temperature REAL,
    precipitation REAL,
    PRIMARY KEY (city, date)
);
""")

# Insert rows (idempotent)
city = "Bangalore"
for i, date in enumerate(data["daily"]["time"]):
    temp = data["daily"]["temperature_2m_max"][i]
    precip = data["daily"]["precipitation_sum"][i]
    cur.execute("""
        INSERT INTO raw_weather (city, date, temperature, precipitation)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (city, date) DO NOTHING;
    """, (city, date, temp, precip))

conn.commit()
cur.close()
conn.close()
print(f"✅ Data loaded into Postgres for {start_date} → {end_date}!")
