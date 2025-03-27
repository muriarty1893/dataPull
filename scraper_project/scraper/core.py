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
                    }
                    
                    # Add all product details as separate columns
                    products_data.update(product_details_dict)
                    
                    page_data.append(products_data)
                    products_on_page += 1
                    # Create a more comprehensive display format for the product with newlines
                    price_display = product_details_dict.get("Price", "Not available")
                    full_product_info = f"Brand: {product_name_clear}\nModel: {product_name_1_clear}\nPrice: {price_display}"
                    reporting.print_product_scraped(full_product_info)
    
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
    
    # Drop the originalPrice column if it exists (it will be empty)
    if 'originalPrice' in df.columns:
        df = df.drop('originalPrice', axis=1)
    
    # Translate column names from Turkish to English
    column_translations = {
        # Keep original columns
        'link': 'link',
        'brand': 'brand',
        'product': 'product',
        'Price': 'price',
        
        # Translate Turkish to English
        'Garanti Tipi': 'warranty_type',
        'Dahili Hafıza': 'internal_storage',
        'RAM Kapasitesi': 'ram_capacity',
        'Ekran Boyutu': 'screen_size',
        'Pil Gücü (mAh)': 'battery_power_mah',
        'Mobil Bağlantı Hızı': 'mobile_connection_speed',
        'Ön Kamera Çözünürlüğü': 'front_camera_resolution',
        'Kamera Çözünürlüğü': 'camera_resolution',
        'Ön Kamera Sayısı': 'front_camera_count',
        'Ekran Çözünürlüğü': 'screen_resolution',
        'Ekran Teknolojisi': 'screen_technology',
        'Ön Kamera Çözünürlük Aralığı': 'front_camera_resolution_range',
        'Görüntü Teknolojisi': 'display_technology',
        'Ana Kamera Flaş': 'main_camera_flash',
        'Ön Kamera Flaş': 'front_camera_flash',
        'Ekran Cinsi': 'screen_type',
        'Arka Kamera Sayısı': 'rear_camera_count',
        'Ekran Boyut Aralığı': 'screen_size_range',
        'İşletim Sistemi': 'operating_system',
        'Çift Hat': 'dual_sim',
        'Kablosuz Şarj': 'wireless_charging',
        'Yüz Tanıma': 'face_recognition',
        'Dokunmatik Ekran': 'touchscreen',
        'Garanti Süresi': 'warranty_period',
        'Şarj Girişi': 'charging_port',
        'Ana Kamera Çözünürlük Aralığı': 'main_camera_resolution_range',
        'NFC': 'nfc',
        'Ekran Yenileme Hızı': 'screen_refresh_rate',
        'Kulaklık Girişi': 'headphone_jack',
        'Şarj Hızı': 'charging_speed',
        'Arttırılabilir Hafıza (Hafıza Kartı Desteği)': 'expandable_storage',
        'Batarya Kapasitesi Aralığı': 'battery_capacity_range',
        'Parmak İzi Okuyucu': 'fingerprint_reader',
        'Suya/Toza Dayanıklılık': 'water_dust_resistance',
        'Renk': 'color',
        'Yapay Zeka': 'artificial_intelligence',
        'Video Kayıt Çözünürlüğü': 'video_recording_resolution',
        'Menşei': 'country_of_origin',
        'Cep Telefonu Modeli': 'phone_model',
        'Radio': 'radio',
        'CPU Aralık': 'cpu_range',
        'Görüntülü Konuşma': 'video_call',
        'Kozmetik Durum': 'cosmetic_condition',
        'Tamir Edilebilirlik': 'repairability',
        'CE Uygunluk Sembolu': 'ce_compliance',
        'İthalatçı/ Yetkili Temsilci/ İfa Hizmet Sağlayıcı': 'importer_representative',
        'Üretici Bilgisi': 'manufacturer_info'
    }
    
    # Rename columns with English names
    df = df.rename(columns=lambda x: column_translations.get(x, x))
    
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