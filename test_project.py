"""
Unit tests for the BitcoinAnalyser project.

This file contains pytest-based tests for:
- validation helpers
- user input helpers
- class initialization
- API wrapper function
- data fetching
- CSV saving
- statistics calculation
- chart generation
- PDF export
- interactive main loop exit behavior

The tests use mocking so external APIs, file I/O, and interactive input
do not affect the test run.
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open

import project


def test_validate_days():
    assert project.validate_days(1) is True
    assert project.validate_days("99") is True
    assert project.validate_days(0) is False
    assert project.validate_days(100) is False
    assert project.validate_days("abc") is False


def test_validate_currency():
    assert project.validate_currency("inr") is True
    assert project.validate_currency("USD") is True
    assert project.validate_currency("us") is False
    assert project.validate_currency("usdt") is False


def test_get_days_from_user():
    with patch("builtins.input", side_effect=["0", "10"]):
        assert project.get_days_from_user() == 10


def test_get_currency_from_user():
    with patch("builtins.input", side_effect=["u", "inr"]):
        assert project.get_currency_from_user() == "inr"


def test_init():
    obj = project.BitcoinAnalyser(days=5, currency="usd")
    assert obj.days == 5
    assert obj.currency == "usd"
    assert obj.current_price is None
    assert obj.time_price == []
    assert obj.stats_data == {}


def test_fetch_data():
    obj = project.BitcoinAnalyser()

    current = {"bitcoin": {"inr": 123.45}}
    market = {"prices": [[1710000000000, 100.0], [1710003600000, 110.0]]}

    with patch.object(obj, "_get_json", side_effect=[current, market]):
        obj.fetch_data()

    assert obj.current_price == 123.45
    assert len(obj.time_price) == 2


def test_save_prices():
    obj = project.BitcoinAnalyser()
    obj.time_price = [[project.datetime(2026, 5, 20, 10, 0, 0), 100.0]]

    m = mock_open()
    with patch("builtins.open", m):
        obj.save_prices("x.csv")

    m.assert_called_once()


def test_calculate_statistics():
    obj = project.BitcoinAnalyser()
    obj.time_price = [
        [project.datetime(2026, 5, 20, 10, 0, 0), 10.0],
        [project.datetime(2026, 5, 20, 11, 0, 0), 20.0],
    ]

    obj.calculate_statistics()

    assert obj.stats_data["Average"] == 15.0
    assert obj.stats_data["Median"] == 15.0
    assert obj.stats_data["Max"] == 20.0
    assert obj.stats_data["Min"] == 10.0
    assert obj.stats_data["Growth %"] == 100.0


def test_generate_line_diagram():
    obj = project.BitcoinAnalyser()
    obj.time_price = [
        [project.datetime(2026, 5, 20, 10, 0, 0), 10.0],
        [project.datetime(2026, 5, 20, 11, 0, 0), 20.0],
    ]

    with patch("project.plt.savefig") as mocked_save, patch("project.plt.close"):
        obj.generate_line_diagram("plot.png")

    mocked_save.assert_called_once_with("plot.png", dpi=150)


def test_export_report():
    obj = project.BitcoinAnalyser()
    obj.current_price = 100.0
    obj.time_price = [
        [project.datetime(2026, 5, 20, 10, 0, 0), 10.0],
        [project.datetime(2026, 5, 20, 11, 0, 0), 20.0],
    ]
    obj.stats_data = {
        "Average": 15.0,
        "Median": 15.0,
        "Max": 20.0,
        "Min": 10.0,
        "Volatility": 7.07,
        "Growth %": 100.0,
    }

    fake_pdf = MagicMock()
    with patch("project.FPDF", return_value=fake_pdf):
        obj.export_report("report.pdf")

    fake_pdf.output.assert_called_once_with("report.pdf")


def test_main_exit():
    with patch("project.Figlet") as mocked_figlet, patch(
        "builtins.input", side_effect=["6", ""]
    ), patch("project.print"):
        mocked_figlet.return_value.renderText.return_value = "TITLE"
        project.main()
