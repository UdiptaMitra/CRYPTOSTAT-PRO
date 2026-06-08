"""
CRYPTOSTAT PRO : Bitcoin Analytics Toolkit

This project fetches live and historical Bitcoin price data from CoinGecko via API,
saves the data to CSV, calculates summary statistics, generates a line chart, and exports a PDF report.
"""

import csv
import re
import statistics
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import requests
from fpdf import FPDF
from pyfiglet import Figlet
from tabulate import tabulate

# Directories
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"

# API endpoint for current Bitcoin price.
COINGECKO_SIMPLE_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"

# API endpoint for Bitcoin historical market data.
COINGECKO_MARKET_CHART_URL = (
    "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
)

# Default currency used when user input is invalid.
DEFAULT_CURRENCY = "inr"

# Default number of days used when user input is invalid.
DEFAULT_DAYS = 1

# Maximum time in seconds to wait for each API request.
REQUEST_TIMEOUT = 15

# Supported fiat currencies by CoinGecko for this program.
SUPPORTED_CURRENCIES = {
    "usd",
    "aed",
    "ars",
    "aud",
    "bdt",
    "bhd",
    "bmd",
    "brl",
    "cad",
    "chf",
    "clp",
    "cny",
    "czk",
    "dkk",
    "eur",
    "gbp",
    "gel",
    "hkd",
    "huf",
    "idr",
    "ils",
    "inr",
    "jpy",
    "krw",
    "kwd",
    "lkr",
    "mmk",
    "mxn",
    "myr",
    "ngn",
    "nok",
    "nzd",
    "php",
    "pkr",
    "pln",
    "rub",
    "sar",
    "sek",
    "sgd",
    "thb",
    "try",
    "twd",
    "uah",
    "vef",
    "vnd",
    "zar",
    "xdr",
}


def validate_days(days):
    """
    Validate the number of days entered by the user.

    Args:
        days: The value entered by the user for the number of days.

    Returns:
        True if the value is an integer between 1 and 99, otherwise False.
    """
    try:
        value = int(str(days).strip())
    except ValueError:
        return False
    return 1 <= value <= 99


def validate_currency(currency):
    """
    Validate the currency code entered by the user.

    Args:
        currency: The currency code entered by the user.

    Returns:
        True if the value is exactly three alphabetic characters, otherwise False.
    """
    return bool(re.fullmatch(r"[A-Za-z]{3}", currency.strip()))


class BitcoinAnalyser:
    """
    Fetch, process, visualize, save, and export Bitcoin analytics data.

    This class stores the current price, historical time-series data, and
    computed statistics for Bitcoin based on user-selected days and currency.
    """

    def __init__(self, days=DEFAULT_DAYS, currency=DEFAULT_CURRENCY):
        """
        Initialize the analyser with days and currency settings.

        Args:
            days: Number of days of historical data to fetch.
            currency: Three-letter currency code.
        """
        self.days = days
        self.currency = currency.lower().strip()
        self.current_price = None
        self.time_price = []
        self.stats_data = {}

        if not validate_days(self.days):
            print("Invalid days input. Using default value: 1")
            self.days = DEFAULT_DAYS

        if not validate_currency(self.currency):
            print("Invalid currency format. Using default value: INR")
            self.currency = DEFAULT_CURRENCY

        if self.currency not in SUPPORTED_CURRENCIES:
            print("Currency not supported by CoinGecko. Using default value: INR")
            self.currency = DEFAULT_CURRENCY

    def _get_json(self, url, params):
        """
        Send a GET request and return the JSON data.

        Args:
            url: The API endpoint to call.
            params: Query parameters to send with the request.

        Returns:
            JSON response as a dictionary.

        Raises:
            requests.RequestException: If the HTTP request fails.
        """
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def fetch_data(self):
        """
        Fetch the current Bitcoin price and historical price data.
        The current price is retrieved from the simple price endpoint.
        Historical prices are retrieved from the market chart endpoint and
        stored as a list of [datetime, price] rows.
        """
        print(f"Current price of Bitcoin in {self.currency.upper()}:")

        # Fetch current price.
        try:
            data = self._get_json(
                COINGECKO_SIMPLE_PRICE_URL,
                {"ids": "bitcoin", "vs_currencies": self.currency},
            )
            self.current_price = float(data["bitcoin"][self.currency])
            print(self.current_price)
        except (requests.RequestException, KeyError, TypeError, ValueError):
            print("Could not fetch current price.")
            self.current_price = None
        print()

        print(
            f"Time series price data of {self.days} day(s) in {self.currency.upper()}:"
        )

        # Fetch historical prices.
        try:
            data = self._get_json(
                COINGECKO_MARKET_CHART_URL,
                {"vs_currency": self.currency, "days": self.days},
            )
            prices = data.get("prices", [])

            # Convert raw timestamp pairs into readable datetime objects.
            self.time_price = [
                [datetime.fromtimestamp(ts / 1000), float(price)]
                for ts, price in prices
            ]

            if not self.time_price:
                raise ValueError("No historical data returned.")

            # Display the historical data in a clean table.
            print(
                tabulate(
                    [
                        [dt.strftime("%Y-%m-%d %H:%M:%S"), f"{price:.2f}"]
                        for dt, price in self.time_price
                    ],  # Formatting of date and price
                    headers=["Date", "Price"],
                    tablefmt="grid",
                    stralign="center",
                    numalign="center",
                )
            )
        except (requests.RequestException, KeyError, TypeError, ValueError):
            print("Could not fetch historical data.")
            self.time_price = []

    def save_prices(self, filename=OUTPUT_DIR / "saved_records.csv"):
        """
        Save the fetched historical data to a CSV file.

        Args:
            filename: Name of the CSV file to write.
        """
        if not self.time_price:
            print("No data available to save.")
            return

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Write the stored time series data to file.
        try:
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Price"])
                for row in self.time_price:
                    writer.writerow([row[0].isoformat(sep=" "), row[1]])
                    # ISO format stores the date-time ss readable text instead of a raw datetime object
            print(f"Successfully saved {len(self.time_price)} records to '{filename}'.")
        except (OSError, IOError):
            print("Could not write to file.")

    def calculate_statistics(self):
        """
        Calculate summary statistics from the fetched Bitcoin prices.
        The statistics include average, median, maximum, minimum, volatility, and percentage growth across the fetched series.
        """
        if not self.time_price:
            print("No data available to calculate statistics.")
            return

        # Extract only the price values from the stored rows.
        prices = [float(row[1]) for row in self.time_price]

        if not prices:
            print("No usable data after outlier cleaning.")
            return

        # Calculate statistical summary values.
        avg_p = statistics.mean(prices)
        med_p = statistics.median(prices)
        max_p = max(prices)
        min_p = min(prices)
        vol = statistics.stdev(prices) if len(prices) > 1 else 0.0
        growth = ((prices[-1] - prices[0]) / prices[0]) * 100 if prices[0] else 0.0

        # Store the values for later report generation.
        self.stats_data = {
            "Average": avg_p,
            "Median": med_p,
            "Max": max_p,
            "Min": min_p,
            "Volatility": vol,
            "Growth %": growth,
        }

        # Print the statistics in a formatted table.
        print(
            tabulate(
                [
                    [
                        f"{avg_p:.2f}",
                        f"{med_p:.2f}",
                        f"{max_p:.2f}",
                        f"{min_p:.2f}",
                        f"{vol:.2f}",
                        f"{growth:+.2f}%",
                    ]
                ],
                headers=["Average", "Median", "Max", "Min", "Volatility", "Growth %"],
                tablefmt="grid",
                stralign="center",
                numalign="center",
            )
        )

    def generate_line_diagram(self, filename=OUTPUT_DIR / "line_diag.png"):
        """
        Generate and save a line chart of the Bitcoin price trend.

        Args:
            filename: Name of the image file to save.
        """
        if not self.time_price:
            print("No data available to plot.")
            return

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Split stored rows into separate x and y values.
        dates = [row[0] for row in self.time_price]
        prices = [float(row[1]) for row in self.time_price]

        # Create the price trend chart with the help og matplotlib.
        plt.figure(figsize=(12, 5))
        plt.plot(dates, prices, color="green", linewidth=2)
        plt.title(
            f"Bitcoin Price Trend for {self.days} day(s) in {self.currency.upper()}"
        )
        plt.xlabel("Time")
        plt.ylabel(f"Price ({self.currency.upper()})")
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()
        print(f"Line diagram saved to '{filename}'.")

    def export_report(self, filename=OUTPUT_DIR / "Bitcoin_Analytics_Report.pdf"):
        """
        Export a formatted PDF report containing price data, statistics,
        market inferences, and the chart image.

        Args:
            filename: Name of the PDF file to generate.
        """
        if self.current_price is None or not self.time_price or not self.stats_data:
            print("Fetch data and calculate statistics before exporting the report.")
            return

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Create the PDF document.
        pdf = FPDF()
        pdf.add_page()

        basher_font = ASSETS_DIR / "basher_rivelga.ttf"
        georgia_font = ASSETS_DIR / "georgia.ttf"
        georgia_bold_font = ASSETS_DIR / "georgiab.ttf"

        # Register custom fonts for the report.
        pdf.add_font("BasherRivelga", "", str(basher_font), uni=True)
        pdf.add_font("Georgia", "", str(georgia_font), uni=True)
        pdf.add_font("Georgia", "B", str(georgia_bold_font), uni=True)

        # Title heading.
        pdf.set_text_color(34, 139, 34)
        pdf.set_font("BasherRivelga", "", 22)
        pdf.cell(0, 14, "CRYPTOSTAT PRO: ANALYTICS REPORT", ln=True, align="C")

        pdf.ln(3)

        # Live price heading and value.
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Georgia", "B", 14)
        pdf.cell(
            0,
            10,
            f"Live Price: {self.current_price:.2f} {self.currency.upper()}",
            ln=True,
            align="C",
        )

        pdf.ln(4)

        # Statistics section heading.
        pdf.set_text_color(34, 139, 34)
        pdf.set_font("Georgia", "B", 13)
        pdf.cell(0, 9, "Market Statistics Summary:", ln=True)
        pdf.ln(1)

        # Table headers.
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Georgia", "B", 11)
        pdf.set_fill_color(220, 260, 220)
        pdf.cell(95, 10, "Statistical Summary", border=1, align="C", fill=True)
        pdf.cell(95, 10, "Value", border=1, align="C", fill=True, ln=True)

        # Table rows.
        pdf.set_font("Georgia", "", 11)
        for key, value in self.stats_data.items():
            pdf.set_fill_color(235, 245, 235)
            value_text = f"{value:+.2f}%" if key == "Growth %" else f"{value:.2f}"
            pdf.cell(95, 10, key, border=1, align="C", fill=True)
            pdf.cell(95, 10, value_text, border=1, align="C", fill=True, ln=True)

        pdf.ln(8)

        # Market inferences heading and text.
        pdf.set_text_color(34, 139, 34)
        pdf.set_font("Georgia", "B", 13)
        pdf.cell(0, 9, "Market Inferences:", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Georgia", "", 11)

        growth_val = self.stats_data.get("Growth %", 0.0)
        vol_val = self.stats_data.get("Volatility", 0.0)
        avg_val = self.stats_data.get("Average", 0.0)

        # Trend inference.
        if growth_val >= 0:
            pdf.multi_cell(
                0,
                8,
                f"- The asset shows a bullish trend with a {growth_val:.2f}% increase.",
            )
        else:
            pdf.multi_cell(
                0,
                8,
                f"- The asset shows a bearish trend with a {growth_val:.2f}% decrease.",
            )

        # Volatility inference.
        if vol_val > (avg_val * 0.05):
            pdf.multi_cell(
                0,
                8,
                "- High volatility detected: market conditions are relatively risky.",
            )
        else:
            pdf.multi_cell(
                0, 8, "- Low volatility detected: price movement is relatively stable."
            )

        pdf.ln(8)

        # Graphical section heading.
        pdf.set_text_color(34, 139, 34)
        pdf.set_font("Georgia", "B", 13)
        pdf.cell(0, 9, "Graphical Representation of Price Trend", ln=True)
        pdf.ln(4)

        # Add the saved chart image to the report.
        chart_path = OUTPUT_DIR / "line_diag.png"
        try:
            pdf.image(str(chart_path), x=15, w=180)
        except Exception:
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Georgia", "", 11)
            pdf.cell(
                0, 8, "Visual chart file not found or could not be embedded.", ln=True
            )

        # Save the completed PDF to file.
        try:
            pdf.output(str(filename))
            print(f"Report exported successfully as '{filename}'.")
        except Exception:
            print("Failed to export PDF.")


def get_days_from_user():
    """
    Prompt the user until a valid day value is entered.

    Returns:
        An integer between 1 and 99.
    """
    while True:
        days_input = input("Enter days (atmost 2-digit number, 1-99): ").strip()
        if validate_days(days_input):
            return int(days_input)
        print("Invalid days. Please enter a number between 1 and 99.")


def get_currency_from_user():
    """
    Prompt the user until a valid three-letter currency code is entered.

    Returns:
        A lowercase three-letter currency string.
    """
    while True:
        currency_input = input("Enter currency code (3 letters): ").strip()
        if validate_currency(currency_input):
            return currency_input.lower()
        print("Invalid currency. Please enter exactly 3 letters.")


def main():
    """
    Run the interactive Bitcoin analytics menu.

    The user can choose to fetch data, save prices, view statistics, generate a chart,
    or export a PDF report.
    """
    analyser = BitcoinAnalyser()
    figlet = Figlet(font="chunky")

    while True:
        # Print the styled title and menu on each loop iteration.
        print(figlet.renderText("CRYPTOSTAT PRO"))
        print(f"{'Bitcoin Analytics Toolkit':^37}")
        print("=" * 36, "\n")

        menu_options = [
            ["1", "Fetch Bitcoin Data"],
            ["2", "Save Fetched Prices"],
            ["3", "View Statistics"],
            ["4", "Generate Visual Chart"],
            ["5", "Export Report"],
            ["6", "Exit"],
        ]

        print(
            tabulate(
                menu_options,
                headers=["Option", "Task"],
                tablefmt="grid",
                stralign="center",
                numalign="center",
            )
        )

        choice = input("\nEnter your choice: ").strip()

        match choice:
            case "1":
                days = get_days_from_user()
                currency = get_currency_from_user()
                analyser = BitcoinAnalyser(days=days, currency=currency)
                analyser.fetch_data()
            case "2":
                analyser.save_prices()
            case "3":
                analyser.calculate_statistics()
            case "4":
                analyser.generate_line_diagram()
            case "5":
                analyser.export_report()
            case "6":
                print("Exiting program.")
                break
            case _:
                print("Invalid choice. Please select a valid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
