import csv
import os
import sys
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "holdings.csv")

def read_holdings():
    holdings = []
    try:
        with open(CSV_PATH, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                row["units"] = float(row["units"])
                row["target_allocation"] = float(row["target_allocation"])
                holdings.append(row)
        return holdings
    except FileNotFoundError:
        print(f"Error: could not find holdings file at {CSV_PATH}")
        sys.exit(1)

def get_latest_nav(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)
    data = response.json()

    latest_entry = data["data"][0]["nav"]
    nav = float(latest_entry)
    return nav

print(get_latest_nav(122639))