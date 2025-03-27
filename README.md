# Trendyol Product Scraper

A modular, well-structured scraper for collecting product details from Trendyol.com to be used for machine learning price prediction.<br>
Currently Phones (https://www.trendyol.com/cep-telefonu-x-c103498?pi=) 

## Project Structure

```
/
├── README.md               # This file
├── scraper_project/        # Main project directory
│   ├── main.py             # Entry point script
│   └── scraper/            # Main package
│       ├── __init__.py     # Package initializer
│       ├── core.py         # Core scraping functionality
│       ├── parser.py       # HTML parsing functions
│       ├── reporting.py    # Functions for printing messages and reports
│       ├── utils.py        # Utility functions
│       └── config/         # Configuration package
│           ├── __init__.py # Config package initializer
│           └── settings.py # Configurable settings
└── output/                 # Directory for output CSV files
```

## Features

- Modular and maintainable code structure
- Extracts product details into separate columns for machine learning
- Timing and performance measurement tools
- Command-line interface for flexible usage
- Error handling and reporting

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

### With Profiling

```bash
python -m scraper_project.main --profile
```

## Configuration

You can adjust the following settings in `scraper/config/settings.py`:

- `BASE_URL`: The base URL to scrape from
- `START_PAGE`: Default starting page number
- `END_PAGE`: Default ending page number
- `MIN_DELAY` and `MAX_DELAY`: Random delay between requests
- `OUTPUT_FILE`: Default output filename
- HTML selectors and CSS classes

## Output Data

The scraper extracts various product details, including:

- Brand
- Product name
- Price
- Internal storage
- RAM capacity
- Screen size
- Battery capacity
- Other phone specifications

Each feature is stored in its own column, making the data ready for machine learning applications.

## Performance Optimization

The scraper includes timing utilities to help optimize performance:

- Total execution time
- Average time per page
- Average time per product
- Detailed profiling with cProfile

## Dependencies

- requests
- beautifulsoup4
- pandas 
