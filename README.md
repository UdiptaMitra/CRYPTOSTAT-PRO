<div align="center">

# CS50P Final Project: CRYPTOSTAT PRO
### Bitcoin Analytics and Financial Reporting Toolkit

![Python](https://img.shields.io/badge/Python-3x+-green?style=for-the-badge&logo=python&logoColor=green)
![Harvard](https://img.shields.io/badge/Harvard-CS50P-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

**Author:** Udipta Mitra
**Video Demo:** https://youtu.be/QSErKUouEQw

![App Screenshot](assets/pic.jfif)
</div>



<br>

## Overwiew

**CRYPTOSTAT PRO** is a command-line Python application that fetches Bitcoin market data, processes historical prices, calculates useful statistics, generates a line chart, and exports a clean PDF report. The CoinGecko API is used for fetching live and historical data and Object-Oriented Programming is applied to keep the project organized and testable.

<br>

## Project Structure

```
project/
│
├── project.py                        # Core Application (Main Loop & Logic)
├── test_project.py                   # Pytest Unit Tests (Mock Frameworks)
├── README.md                         # Documentation
├── requirements.txt                  # Project Dependencies
│
├── assets/                           # Fonts (no liscense)
│   ├── basher_rivelga.ttf            # Main Heading Display Font
│   ├── georgia.ttf                   # Body Font
│   └── georgiab.ttf                  # Subheading Display Font
│
└── output/                           # Generated Output Files
    ├── saved_records.csv             # Structured Historical Data
    ├── line_diag.png                 # Trend Chart Image
    └── Bitcoin_Analytics_Report.pdf  # Final Summary PDF Report
```

<br>

## File Overview

### `project.py`

```
project.py
│
├── validate_days()                  # Validates if input is an integer between 1 and 99 (upper limit to prevent memory load or performance lag.)
├── validate_currency()              # Validates if input matches a 3-letter alphabetic pattern via regex
├── get_days_from_user()             # Prompts user via loop until validate_days passes
├── get_currency_from_user()         # Prompts user via loop until validate_currency passes
│
├── class BitcoinAnalyser            # Class handling data application logic
│   ├── __init__()                   # Sets defaults and applies validation
│   ├── _get_json()                  # Executes get requests (Protected)
│   ├── fetch_data()                 # Queries API for live and time-series historical data
│   ├── save_prices()                # Writes in-memory data rows directly to a local CSV file
│   ├── calculate_statistics()       # Computes statistical summaries using the statistics module
│   ├── generate_line_diagram()      # Renders and saves a time-series price trend chart
│   └── export_report()              # Compiles tables, charts, and text into a final summary PDF
│
└── main()                           # Runs the interactive terminal menu loop
```

* **Input Validation Layer:** User inputs are checked by the `validate_days` and `validate_currency` functions, with regular expressions utilized to match 3-letter currency formats and day ranges.
* **User Interaction Loop:**  `while True` loops are run by the input functions `get_days_from_user` and `get_currency_from_user`, where the user is prompted until valid data is entered. Inside `main()`, `match/case` statement within the loop for user input.
* **The BitcoinAnalyser Class:** Data is centrally controlled by this class. Data retrieval, finding inferences and displaying output is done by this class.
* **Statistical Analysis:** Prices are extracted into lists by the `calculate_statistics` method, and statistical summaries—including the average, median, minimum, maximum, volatility, and percentage growth are computed via the `statistics` module.
* **Charts and PDF Reports:** Visuals and document generation are handled by `generate_line_diagram` and `export_report`. Historical price trends are plotted as a line diagram using `matplotlib`, and a compiled PDF is laid out using `fpdf`.
---

### `test_project.py`
```
test_project.py
│
├── test_validate_days()           # Verifies boundary cases and true/false limits
├── test_validate_currency()       # Asserts valid alphabetic strings and filters bad input lengths
├── test_get_days_from_user()      # Mocks input loops to test validation behavior
├── test_get_currency_from_user()  # Captures terminal streams to verify loop traps for invalid strings
├── test_init()                    # Validates default state assignments inside object memory
│
├── test_fetch_data()              # Mocks API JSON payloads to verify data parsing
├── test_save_prices()             # Controls system I/O
├── test_calculate_statistics()    # Asserts calculations match exact expectations using fixed arrays
├── test_generate_line_diagram()   # Verifies plot generation without writing files to disk
├── test_export_report()           # Tracks internal document structure actions
└── test_main_exit()               # Captures interactive menu choices to safely trigger termination
```

* **Helper Validation Tests (test_validate_days, test_validate_currency):** Helper functions are checked by these tests by passing normal integer strings, floating points, characters, and correct or short alpha strings to make sure input processing is executed perfectly before data is passed onward.
* **User Input Simulation (test_get_days_from_user, test_get_currency_from_user):** A user given bad inputs followed by a correct response is simulated by using `unittest.mock.patch` on `builtins.input`. It is verified by these test functions that loops are run by the input functions that stay active until a proper value is entered.
* **Object Initialization & State Checks (test_init):** Loading of instance attributes by the BitcoinAnalyser constructor is checked by this test. It is validated that the days and currency variables are passed into memory correctly, and that clear, safe configurations are used to initialize list, dictionary, and price state buckets.
* **API Network Mocking (test_fetch_data):** Internal network methods are intercepted by mock objects to verify that currency keys and lists of pricing arrays are parsed correctly by the application.
* **File I/O and System Mocking (test_save_prices, test_generate_line_diagram, test_export_report):** Standard built-in functions from matplotlib and FPDF are mocked by these tests to verify that export streams are executed correctly.
* **Mathematical Accuracy (test_calculate_statistics):** Calculation accuracy is checked by this test by feeding a predefined date-and-price matrix into the processing engine. Tests are run on the final outcomes to verify the calculations.
* **Interactive Menu Lifecycles (test_main_exit):** Terminal main execution flows are checked by mocking input signals.


<br>

## Installation & Use


* Open the terminal inside the project directory.
* Install the dependencies:
```bash
pip install -r requirements.txt
```
* Run the main program:
```
python project.py
```
* Enter the number of days for historical Bitcoin data to retrieve.
* Enter a 3-letter alphabetic pattern (currency code)
* Use the menu options to:
  * Fetch Bitcoin data
  * Save prices to CSV
  * Calculate statistics
  * Generate a line chart
  * Export the PDF report
  * Exit the program
* Generated files will be saved inside the output/ folder.
* To install and run this project locally, ensure you have Python 3.x installed along with the required libraries.
* Run the test_project.py file by:
```
pytest test_project.py
```
#### **External Libraries Used (requirements.txt):**

*   fpdf2==2.8.7 and fpdf==1.7.2 — For assembling and rendering the PDF report documents.
*   matplotlib==3.10.9 — For plotting historical time-series pricing data.
*   pyfiglet==1.0.4 — For generating large ASCII text banners in the terminal menu.
*   requests==2.34.2 — For managing HTTP network operations with the CoinGecko API.
*   tabulate==0.10.0 — For formatting data tables neatly inside the console view.
*   pytest==9.0.3 — For executing the automated testing suite.

#### **Standard Python Modules Used:**

*   csv — For reading and writing historical price lists to disk.
*   re — For parsing inputs with regular expressions.
*   statistics — For running mathematical calculations on extracted arrays.
*   datetime — For translating Unix millisecond timestamps into readable calendar dates.

<br>

## Features

* **API Consumption:** JSON data is fetched from the CoinGecko API with error handling.

 _Simple Price API:_ https://api.coingecko.com/api/v3/simple/price
_Market Chart API (Bitcoin):_ https://api.coingecko.com/api/v3/coins/bitcoin/market_chart
* **Statistical Calculations:** Statistical summaries are calculated using `statistics` module:
  * Arithmetic Mean and Median
  * Price Extrema (Minimum and Maximum prices)
  * Volatility (Sample Standard Deviation)
  * Total Growth Rate (Percentage change across the duration)
* **Line Chart Generation:** `matplotlib` library is used to generate price trend charts with  axis labeling based on the target currency.
* **PDF Report Generation:** All data is compiled into a single-page PDF report.

<br>

## Challenges Encountered

* **Handling Live API Data & JSON Structure**
  * **Challenge:** Data from the CoinGecko API came structured as nested dictionaries and lists containing raw millisecond timestamps.
  * **Resolution:** Implemented Python's built-in `datetime.fromtimestamp()` to convert millisecond timestamps into readable dates.
* **Memory Issues & Cropped Images in Matplotlib**
  * **Challenge:** Generating charts multiple times within a single terminal session caused visual overlapping, high memory retention, and truncated date labels along the bottom axis.
  * **Resolution:** Utilized `plt.tight_layout()` to automatically scale layout elements and prevent text clipping. Added `plt.close()` at the end of the charting routine to clear the active figure from memory after saving.
* **Managing Content Spacing in FPDF**
  * **Challenge:** As the `fpdf` library relies on a strict grid coordinate system (x and y), initial layouts suffered from overlapping text tables, market summary blocks, and chart images.
  * **Resolution:** Mapped out layout positions programmatically using precise line breaks (`pdf.ln()`) and explicitly defined structural dimensions (`w=180`, `x=15`) for the chart placement to constrain all content neatly onto a single page.
* **Learning to Write Unit Tests with Mocks**
  * **Challenge:** Validating functions that depend on live internet connections, real-time user keyboard inputs, or local file writing risked cluttering the local workspace and creating unpredictable test outcomes.
  * **Resolution:** Used `unittest.mock.patch` to isolate dependencies. This approach simulates remote API JSON payloads, mocks keyboard input streams (such as passing a exit flag), and intercepts file writing operations via `mock_open` so `pytest` executes entirely in memory.


<br>

## What I Learned

* Build a command-line Python application.
* Fetch and process data from an API.
* Work with JSON data.
* Convert timestamps into readable dates.
* Validate user input.
* Use Object-Oriented Programming in a real project.
* Generate charts using `matplotlib`.
* Create PDF reports using `fpdf`.
* Save data into CSV files.
* Write tests using `pytest`.
* Use mocks to test input, API calls, and file operations.
* Organize a Python project with separate files and folders.

<br>

## Limitations

* Requires an active internet connection to fetch live and historical Bitcoin data.
* Depends on the availability and response structure of the CoinGecko API.
* The application currently focuses only on Bitcoin and does not compare multiple cryptocurrencies.
* The generated PDF report uses a fixed layout, so very large tables or long text sections may need further formatting adjustments.
* The project does not store data in a database. Historical records are saved only as a CSV file.
* **Warning**  - The statistics are based only on the fetched price data and should not be treated as financial advice.


<br>

## AI Collaboration & Academic Integrity Statement

Throughout this project, I used artificial intelligence as a supportive knowledge partner to help guide my development.

* **Automating Documentation:** I used AI to generate clean, uniform docstrings for the functions.
* **Structuring Test Cases:** I collaborated with AI to sketch out the initial architecture of the `unittest.mock` blocks inside `test_project.py` so they correctly mirror live data streams.
* **Documentation & Code Style Formatting:** I utilized AI assistance to refine, edit, and structure this README file. Additionally, I used the **Black** code formatter to improve code formatting and readability.

The main project idea, module choices, menu design, statistical formulas, OOP structure, and final implementation were completed through my own learning, research, and CS50P course concepts.

<br>

## Acknowledgements

I would like to thank :

* **Harvard University** for making CS50P available to learners worldwide.
* **Prof. David J. Malan** for explaining computer science so clearly and engaging curiosity among his students.
* **The CS50 Community** for support, discussions, and shared learning.

<br>
