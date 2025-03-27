"""
Core module for the scraper.
Contains the main scraping functionality.
"""
import time
import random
import requests
import pandas as pd

from scraper_project.scraper.config import settings
from scraper_project.scraper import reporting
from scraper_project.scraper import parser

def scrape_product(link_element):
    """
    Scrape a single product.
    
    Args:
        link_element: BeautifulSoup object representing a link
        
    Returns:
        dict: Dictionary of product details
    """
    product_start_time = time.time()
    product_details_dict = {}
    
    link_all = parser.extract_product_link(link_element)
    if not link_all:
        return None, None
    
    try:
        # Add a small delay to avoid being blocked
        time.sleep(random.uniform(settings.MIN_DELAY, settings.MAX_DELAY))
        
        detail_response = requests.get(link_all, headers=settings.HEADERS)
        detail_response.raise_for_status()
        
        product_details_dict = parser.parse_product_details(detail_response.content)
    
    except Exception as e:
        reporting.print_error_fetching(link_all, e)
        return None, None
    
    product_time = time.time() - product_start_time
    reporting.print_product_time(product_time)
    
    return link_all, product_details_dict

def scrape_page(page_number):
    """
    Scrape a single page of products.
    
    Args:
        page_number: Page number to scrape
        
    Returns:
        tuple: (list of scraped products, time taken, number of products)
    """
    start_time_page = time.time()
    page_data = []
    products_on_page = 0
    
    url = settings.BASE_URL + str(page_number)
    reporting.print_page_start(page_number)
    
    try:
        response = requests.get(url, headers=settings.HEADERS)
        response.raise_for_status()
        
        products = parser.parse_product_list(response.content)
        
        for product in products:
            product_name_clear, product_name_1_clear, original_price, product_links = parser.extract_product_info(product)
            
            for link in product_links:
                link_all, product_details_dict = scrape_product(link)
                
                if link_all and product_details_dict:
                    # Create the product data with basic info
                    products_data = {
                        "link": link_all,
                        "brand": product_name_clear,
                        "product": product_name_1_clear,
                        "originalPrice": original_price,
                    }
                    
                    # Add all product details as separate columns
                    products_data.update(product_details_dict)
                    
                    page_data.append(products_data)
                    products_on_page += 1
                    reporting.print_product_scraped(product_name_1_clear)
    
    except Exception as e:
        reporting.print_error_processing_page(page_number, e)
        return [], 0, 0
    
    page_time = time.time() - start_time_page
    reporting.print_page_complete(page_number, page_time, products_on_page)
    
    return page_data, page_time, products_on_page

def scrape():
    """
    Scrape products from multiple pages.
    
    Returns:
        pandas.DataFrame: DataFrame containing all scraped product data
    """
    # Start timing the entire process
    start_time_total = time.time()
    
    # Stats for timing analysis
    page_times = []
    all_data = []
    product_count = 0
    
    for page_number in range(settings.START_PAGE, settings.END_PAGE + 1):
        page_data, page_time, products_on_page = scrape_page(page_number)
        
        if page_data:
            all_data.extend(page_data)
            page_times.append(page_time)
            product_count += products_on_page
    
    # Calculate total execution time
    total_execution_time = time.time() - start_time_total
    
    # Convert to DataFrame and clean up
    df = pd.DataFrame(all_data)
    df = df.fillna("")
    
    # Print timing statistics
    stats = {
        'total_execution_time': total_execution_time,
        'page_times': page_times,
        'product_count': product_count,
        'column_count': len(df.columns)
    }
    reporting.print_timing_statistics(stats)
    
    return df 