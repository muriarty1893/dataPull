import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def main():
    base_url = "https://www.trendyol.com/cep-telefonu-x-c103498?pi="
    start_page = 1
    end_page = 10  # Increased to get more data

    # Headers to make request more like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    data = []

    # Start timing the entire process
    start_time_total = time.time()

    # Stats for timing analysis
    page_times = []
    product_count = 0

    for page_number in range(start_page, end_page + 1):
        # Start timing this page
        start_time_page = time.time()
        
        url = base_url + str(page_number)
        try:
            print(f"Processing page {page_number}...")
            r = requests.get(url, headers=headers)
            r.raise_for_status()  # Check if request was successful
            soup = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
            products = soup.find_all("div", attrs={"class": "p-card-wrppr with-campaign-view"})
            
            products_on_page = 0
            for product in products:
                product_links = product.find_all("div", attrs={"class": "card-border"})
                product_name = product.find("div", attrs={"class": "prdct-desc-cntnr"})
                product_name_1 = product.find("span", attrs={"class": "prdct-desc-cntnr-name hasRatings"})
                product_name_clear = product_name.text.strip() if product_name else None
                product_name_1_clear = product_name_1.text.strip() if product_name_1 else None
                
                # Try to extract price - multiple possible locations
                product_price = product.find("div", attrs={"class": "prc-box-dscntd"})
                if not product_price:
                    product_price = product.find("div", attrs={"class": "prc-box-sllng"})
                original_price = product_price.text.strip() if product_price else None
                
                # Create a dictionary to store product details
                product_details_dict = {}
                
                for link in product_links:
                    link_continue = link.find("a")
                    if link_continue:
                        product_start_time = time.time()
                        
                        link_continue = link_continue.get("href")
                        link_all = f"https://www.trendyol.com{link_continue}"
                        
                        try:
                            # Add a small delay to avoid being blocked
                            time.sleep(random.uniform(0.5, 1.5))
                            
                            detail = requests.get(link_all, headers=headers)
                            detail.raise_for_status()
                            detail_soup = BeautifulSoup(detail.content, "html.parser")
                            
                            # Get main specifications
                            product_specifications = detail_soup.find_all("ul", class_="detail-attr-container")
                            for specific in product_specifications:
                                details = specific.find_all("li", class_="detail-attr-item")
                                for i in details:
                                    label_element = i.find("span")
                                    value_element = i.find("b")
                                    
                                    if label_element and value_element:
                                        label = label_element.text.strip()
                                        value = value_element.text.strip()
                                        # Store each detail as a key-value pair in the dictionary
                                        product_details_dict[label] = value
                        
                            # Additional attempt to extract product specifications from other sections
                            # Some sites have specs in tables
                            spec_tables = detail_soup.find_all("table", class_="product-features")
                            for table in spec_tables:
                                rows = table.find_all("tr")
                                for row in rows:
                                    cells = row.find_all("td")
                                    if len(cells) >= 2:
                                        label = cells[0].text.strip()
                                        value = cells[1].text.strip()
                                        product_details_dict[label] = value
                        
                            # Look for product features section (common on many e-commerce sites)
                            feature_divs = detail_soup.find_all("div", class_="product-feature")
                            for div in feature_divs:
                                label_elem = div.find("span", class_="feature-name")
                                value_elem = div.find("span", class_="feature-value")
                                if label_elem and value_elem:
                                    label = label_elem.text.strip()
                                    value = value_elem.text.strip()
                                    product_details_dict[label] = value
                        
                            # Sometimes specs are in a description section as structured text
                            description = detail_soup.find("div", class_="product-description")
                            if description:
                                desc_text = description.text
                                # Look for common phone specs pattern like "RAM: 8GB"
                                common_specs = [
                                    ("RAM", r"RAM:\s*(\d+\s*GB)"),
                                    ("Storage", r"Storage:\s*(\d+\s*GB)"),
                                    ("Camera", r"Camera:\s*(\d+\s*MP)"),
                                    ("Battery", r"Battery:\s*(\d+\s*mAh)")
                                ]
                                import re
                                for spec_name, pattern in common_specs:
                                    match = re.search(pattern, desc_text)
                                    if match and spec_name not in product_details_dict:
                                        product_details_dict[spec_name] = match.group(1)
                        
                        except Exception as e:
                            print(f"Error fetching details for {link_all}: {e}")
                            continue
                        
                        product_time = time.time() - product_start_time
                        print(f"  Product scraped in {product_time:.2f} seconds")
                
                # Create the product data with basic info
                products_data = {
                    "link": link_all,
                    "brand": product_name_clear,
                    "product": product_name_1_clear,
                    "originalPrice": original_price,
                }
                
                # Add all product details as separate columns
                products_data.update(product_details_dict)
                
                data.append(products_data)
                products_on_page += 1
                product_count += 1
                print(f"Scraped product: {product_name_1_clear}")
            
            # End timing this page
            page_time = time.time() - start_time_page
            page_times.append(page_time)
            print(f"Page {page_number} completed in {page_time:.2f} seconds. Found {products_on_page} products.\n")
                
        except Exception as e:
            print(f"Error processing page {page_number}: {e}")
            continue

    # Calculate total execution time
    total_execution_time = time.time() - start_time_total

    # Convert dataset to a DataFrame
    df = pd.DataFrame(data)

    # Fill missing values with empty string to make it clear they're missing
    df = df.fillna("")

    print(f"\n===== TIMING STATISTICS =====")
    print(f"Total execution time: {total_execution_time:.2f} seconds ({total_execution_time/60:.2f} minutes)")
    print(f"Average time per page: {sum(page_times)/len(page_times):.2f} seconds")
    print(f"Average time per product: {total_execution_time/product_count:.2f} seconds")
    print(f"Total products scraped: {product_count}")
    print(f"Total columns/properties: {len(df.columns)}")
    print(f"===========================\n")

    print(df)

    # Converting it to CSV so we can download
    df.to_csv('trendyol_all_data.csv', encoding="utf-8")
    print("Data saved to trendyol_all_data.csv")
    
    return df

if __name__ == "__main__":
    main()
