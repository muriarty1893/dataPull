# Trendyol Product Scraper

A modular, well-structured scraper for collecting product details from Trendyol.com to be used for machine learning price prediction.

## Dataset Information
- **Source**: Currently scrapes phones from [Trendyol](https://www.trendyol.com/cep-telefonu-x-c103498?pi=)
- **Size**: ~2400 records with 50+ columns of detailed specifications
- **Output**: CSV format with English column headers and original data values

## Project Structure

```
/
├── README.md                   # Project documentation
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore rules
├── scraper_project/            # Main project directory
│   ├── main.py                 # Entry point script
│   └── scraper/                # Main package
│       ├── __init__.py         # Package initializer
│       ├── core.py             # Core scraping functionality
│       ├── parser.py           # HTML parsing functions
│       ├── reporting.py        # Functions for printing messages and reports
│       ├── utils.py            # Utility functions
│       └── config/             # Configuration package
│           ├── __init__.py     # Config package initializer
│           └── settings.py     # Configurable settings
└── output/                     # Directory for output CSV files
    └── trendyol_all_data.csv   # Scraped data output
```

## Features

- Modular and maintainable code structure
- Extracts product details into separate columns for machine learning
- Timing and performance measurement tools
- Command-line interface for flexible usage
- Error handling and reporting
- English column headers with original data values
- Efficiently handles multiple pages
- CSV format for easy data analysis

## Usage

### Basic Usage

```bash
python -m scraper_project.main
```

### Specifying Page Range

```bash
python -m scraper_project.main --start-page 1 --end-page 5
```

### Custom Output File

```bash
python -m scraper_project.main --output custom_filename.csv
```

## Configuration

You can adjust the following settings in `scraper_project/scraper/config/settings.py`:

- `BASE_URL`: The base URL to scrape from
- `START_PAGE`: Default starting page number
- `END_PAGE`: Default ending page number
- `MIN_DELAY` and `MAX_DELAY`: Random delay between requests
- `OUTPUT_FILE`: Default output filename
- HTML selectors and CSS classes

## Output Data

The scraper extracts various product details, including:

- Brand and model information
- Price (in TL)
- Storage capacity and RAM
- Screen specifications (size, resolution, technology)
- Camera details (front/rear, resolution)
- Battery capacity
- Connectivity features (NFC, Bluetooth, etc.)
- And many other phone specifications

Each feature is stored in its own column with English headers, making the data ready for machine learning applications.

## Performance Optimization

The scraper includes timing utilities to help optimize performance:

- Total execution time
- Average time per page
- Average time per product

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- requests >= 2.32.0
- pandas >= 2.2.0
- beautifulsoup4 >= 4.12.0
- bs4 >= 0.0.1
