def print_page_start(page_number):
    print(f"Processing page {page_number}...")

def print_product_time(time_taken):
    print(f"Product scraped in {time_taken:.2f} seconds")

def print_product_scraped(product_name):
    print(f"---\n{product_name}")

def print_page_complete(page_number, time_taken, product_count):
    print(f"Page {page_number} completed in {time_taken:.2f} seconds. Found {product_count} products.\n")

def print_error_fetching(url, error):
    print(f"Error fetching details for {url}: {error}")

def print_error_processing_page(page_number, error):
    print(f"Error processing page {page_number}: {error}")

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
    print(f"o=======================================o\n")

def print_save_confirmation(file_path):
    print(f"Data saved to {file_path}") 