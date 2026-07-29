# driftcheck

A command-line tool that tracks mutual fund portfolio drift against target allocation, using live NAV data.

## Why

Manually checking whether your SIP/mutual fund holdings have drifted from your intended asset allocation means pulling up each fund's NAV, doing the math by hand, and repeating this every time you want to check. `driftcheck` automates this: give it your holdings, it tells you exactly how far off target you are and which funds need rebalancing.

## Features

- Fetches live NAV for Indian mutual funds via the [mfapi.in](https://www.mfapi.in/) API
- Computes current portfolio value, actual allocation %, and drift from target allocation per fund
- Flags any fund that has drifted beyond a configurable threshold
- Sorts the report by drift severity, most out-of-balance fund first
- Saves a timestamped JSON snapshot on every run, building a history over time
- Handles network failures, bad API responses, and malformed input data without crashing

## Installation

```bash
git clone https://github.com/amritxcode/driftcheck.git
cd driftcheck
pip install -r requirements.txt
```

## Usage

1. Edit `data/holdings.csv` with your actual holdings:

```csv
fund_name,scheme_code,units,target_allocation
Parag Parikh Flexi Cap,122639,150.25,40
Kotak Nifty 50,120716,80.50,30
Mirae Asset Nifty Midcap 150 ETF,148649,45.75,20
Junior BeES,118834,10.20,10
```

   - `scheme_code` is the mfapi.in identifier for the fund. Look it up at `https://api.mfapi.in/mf` or search by name.
   - `target_allocation` values should sum to 100 across all rows.

2. Run the tool:

```bash
python driftcheck.py
```

3. Example output:

--- Portfolio Drift Report ---

Total Portfolio Value: ₹29537.24

Kotak Nifty 50
Value: ₹13581.33 | Target: 30.0% | Actual: 45.98% | Drift: 15.98% REBALANCE NEEDED

Mirae Asset Nifty Midcap 150 ETF
Value: ₹572.81 | Target: 20.0% | Actual: 1.94% | Drift: -18.06% REBALANCE NEEDED

Parag Parikh Flexi Cap
Value: ₹13575.27 | Target: 40.0% | Actual: 45.96% | Drift: 5.96% REBALANCE NEEDED

Junior BeES
Value: ₹1807.83 | Target: 10.0% | Actual: 6.12% | Drift: -3.88%

Snapshot saved to snapshots/snapshot_2026-07-29_08-43-47.json

Snapshots are saved to `snapshots/` and are not tracked in version control.

## Error handling

The tool handles several real-world failure cases gracefully rather than crashing:

- Missing or malformed `holdings.csv`
- Network/API unreachable (connection errors, timeouts)
- Invalid or unrecognized scheme codes
- Any other unexpected API response

If a specific fund's NAV can't be fetched, that fund is skipped for the current run and the rest of the portfolio is still processed and reported.

## Project structure
driftcheck/
├── driftcheck.py # main script
├── data/
│ └── holdings.csv # your holdings input
├── snapshots/ # generated JSON snapshots (gitignored)
├── requirements.txt
└── README.md
## Built with

- Python 3
- [requests](https://pypi.org/project/requests/)
- [mfapi.in](https://www.mfapi.in/) — free public API for Indian mutual fund NAV data

## Notes

This was built as a personal tool to automate a check I was already doing manually — not a general-purpose financial product. Scheme codes and thresholds are meant to be edited per person's actual holdings.