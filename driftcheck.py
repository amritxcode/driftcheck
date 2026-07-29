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

def calculate_drift(holdings):
    total_value = 0
    for holding in holdings:
        if "current_value" not in holding:
            continue
        total_value += holding["current_value"]

    for holding in holdings:
        if "current_value" not in holding:
            continue
        actual_allocation = (holding["current_value"] / total_value) * 100
        drift = actual_allocation - holding["target_allocation"]
        holding["actual_allocation"] = actual_allocation
        holding["drift"] = drift

    return holdings

def print_report(holdings, threshold=5):
    print("\n--- Portfolio Drift Report ---\n")
    for holding in holdings:
        if 'current_value' not in holding:
            continue

    
        fund_name = holding["fund_name"]
        current_value = round(holding["current_value"], 2)
        target = holding["target_allocation"]
        actual = round(holding["actual_allocation"], 2)
        drift = round(holding["drift"], 2)

        flag = " REBALANCE NEEDED" if abs(drift) > threshold else ""

        print(f"{fund_name}")
        print(f"  Value: ₹{current_value} | Target: {target}% | Actual: {actual}% | Drift: {drift}%{flag}")
        print()

data = read_holdings()
data = calculate_portfolio(data)
data = calculate_drift(data)
print_report(data)

