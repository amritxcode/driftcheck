import csv
import os
import sys
import requests
import time

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
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        latest_entry = data["data"][0]["nav"]
        nav = float(latest_entry)
        return nav
    except requests.exceptions.RequestException:
        print(f"Error: could not reach API for scheme code {scheme_code}")
        return None 
    except (KeyError, IndexError):
        print(f"Error: unexpected response format for scheme code {scheme_code}")
        return None
    except Exception as e:
        print(f"Unexpected error for scheme code {scheme_code}: {e}")
        return None

def calculate_portfolio(holdings):
    for holding in holdings:
        nav = get_latest_nav(holding["scheme_code"])
        if nav is None:
            print(f"Skipping {holding['fund_name']} - no NAV dala")
            continue
        else:
            current_value = holding["units"]*nav
            holding["current_value"] = current_value
            holding["nav"] = nav
        time.sleep(1)

    return holdings

