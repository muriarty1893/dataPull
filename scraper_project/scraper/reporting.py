"""
Reporting module for the scraper.
Contains functions for printing status updates and statistics.
"""

def print_page_start(page_number):
    """Print a message when starting to process a page."""
    print(f"Processing page {page_number}...")

def print_product_time(time_taken):
    """Print the time taken to scrape a product."""
    print(f"  Product scraped in {time_taken:.2f} seconds")

def print_product_scraped(product_name):
    """Print a message when a product has been scraped."""
    print(f"Scraped product: {product_name}")

def print_page_complete(page_number, time_taken, product_count):
    """Print a message when a page has been completely processed."""
    print(f"Page {page_number} completed in {time_taken:.2f} seconds. Found {product_count} products.\n")

def print_error_fetching(url, error):
    """Print an error message when fetching a product fails."""
    print(f"Error fetching details for {url}: {error}")

def print_error_processing_page(page_number, error):
    """Print an error message when processing a page fails."""
    print(f"Error processing page {page_number}: {error}")

def print_timing_statistics(stats):
    """
    Print timing statistics.
    
    Args:
        stats (dict): Dictionary containing timing statistics with the following keys:
            - total_execution_time: Total time taken to run the scraper
            - page_times: List of times taken for each page
            - product_count: Total number of products scraped
            - column_count: Number of columns/properties extracted
    """
    total_time = stats['total_execution_time']
    page_times = stats['page_times']
    product_count = stats['product_count']
    column_count = stats['column_count']
    
    print(f"\n===== TIMING STATISTICS =====")
    print(f"Total execution time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    
    if page_times:
        print(f"Average time per page: {sum(page_times)/len(page_times):.2f} seconds")
    
    if product_count > 0:
        print(f"Average time per product: {total_time/product_count:.2f} seconds")
    
    print(f"Total products scraped: {product_count}")
    print(f"Total columns/properties: {column_count}")
    print(f"===========================\n")

def print_save_confirmation(file_path):
    """Print a confirmation message when data has been saved."""
    print(f"Data saved to {file_path}") 