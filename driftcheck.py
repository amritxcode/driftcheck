import csv
import os
import sys
import pprint

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