import os
import pandas as pd
from scraper_project.scraper.config import settings

def print_page_start(page_number):
    print(f"Processing page {page_number}...")

def print_product_time(time_taken):
    print(f"Product scraped in {time_taken:.2f} seconds")

def print_product_scraped(product_name):
    print(f"---\n{product_name}")

def print_page_complete(page_number, time_taken, product_count):
    print(f"Page {page_number} completed in {time_taken:.2f} seconds. Found {product_count} products.\n")

def print_timing_statistics(stats):
    total_time = stats['total_execution_time']
    page_times = stats['page_times']
    product_count = stats['product_count']
    column_count = stats['column_count']
    
    print(f"\no========== TIMING STATISTICS ==========O")
    print(f"Total execution time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    
    if page_times:
        print(f"Average time per page: {sum(page_times)/len(page_times):.2f} seconds")
    
    if product_count > 0:
        print(f"Average time per product: {total_time/product_count:.2f} seconds")
    
    print(f"Total products scraped: {product_count}")
    print(f"Total columns/properties: {column_count}")
    print(f"o=======================================o")

def print_save_confirmation(file_path):
    print(f"Data saved to {file_path}") 
    print(f"o=======================================o\n")

def save_to_csv(df, file_path=None):
    if file_path is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'output')
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, settings.OUTPUT_FILE)
    
    df.to_csv(file_path, encoding=settings.OUTPUT_ENCODING)
    print_save_confirmation(file_path)