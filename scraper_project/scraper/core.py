import time
import random
import requests
import pandas as pd
from scraper_project.scraper.config import settings
from scraper_project.scraper import reporting
from scraper_project.scraper import parser

def scrape_product(link_element):
    product_start_time = time.time()
    product_details_dict = {}
    
    link_all = parser.extract_product_link(link_element)
    if not link_all:
        return None, None
    
    time.sleep(random.uniform(settings.MIN_DELAY, settings.MAX_DELAY))
    detail_response = requests.get(link_all, headers=settings.HEADERS)
    product_details_dict = parser.parse_product_details(detail_response.content)
    
    product_time = time.time() - product_start_time
    reporting.print_product_time(product_time)
    
    return link_all, product_details_dict

def scrape_page(page_number):
    start_time_page = time.time()
    page_data = []
    products_on_page = 0
    
    url = settings.BASE_URL + str(page_number)
    reporting.print_page_start(page_number)
    
    if settings.DEBUG:
        print(f"Requesting URL: {url}")
    
    response = requests.get(url, headers=settings.HEADERS)
    if settings.DEBUG:
        print(f"Response status: {response.status_code}")
        print(f"Response length: {len(response.content)} bytes")
    
    products = parser.parse_product_list(response.content)
    
    if settings.DEBUG:
        print(f"Found {len(products)} products on page {page_number}")
    
    for product in products:
        product_name_clear, product_name_1_clear, original_price, product_links = parser.extract_product_info(product)
        
        if settings.DEBUG:
            print(f"Product: {product_name_clear} | {product_name_1_clear} | Links: {len(product_links)}")
        
        for link in product_links:
            link_all, product_details_dict = scrape_product(link)
            
            if link_all and product_details_dict:
                products_data = {
                    "link": link_all,
                    "brand": product_name_clear,
                    "product": product_name_1_clear,
                }
                
                products_data.update(product_details_dict)
                page_data.append(products_data)
                products_on_page += 1
                price_display = product_details_dict.get("Price", "Not available")
                full_product_info = f"Brand: {product_name_clear}\nModel: {product_name_1_clear}\nPrice: {price_display}"
                reporting.print_product_scraped(full_product_info)
    
    page_time = time.time() - start_time_page
    reporting.print_page_complete(page_number, page_time, products_on_page)
    
    return page_data, page_time, products_on_page

def scrape():
    start_time_total = time.time()
    
    page_times = []
    all_data = []
    product_count = 0
    
    for page_number in range(settings.START_PAGE, settings.END_PAGE + 1):
        page_data, page_time, products_on_page = scrape_page(page_number)
        
        if page_data:
            all_data.extend(page_data)
            page_times.append(page_time)
            product_count += products_on_page
    
    total_execution_time = time.time() - start_time_total
    
    df = pd.DataFrame(all_data)
    
    if 'originalPrice' in df.columns:
        df = df.drop('originalPrice', axis=1)
    
    column_translations = {
        'link': 'link',
        'brand': 'brand',
        'product': 'product',
        'Price': 'price',
        
        'Garanti Tipi': 'warranty_type',
        'İşletim Sistemi': 'operating_system',
        'İşlemci Tipi': 'processor_type',
        'İşlemci Nesli': 'processor_generation',
        'RAM': 'ram',
        'Disk Kapasitesi': 'storage_capacity',
        'Disk Türü': 'storage_type',
        'Ekran Boyutu': 'screen_size',
        'Çözünürlük': 'screen_resolution',
        'Ekran Kartı': 'graphics_card',
        'Ekran Kartı Hafızası': 'graphics_memory',
        'Ağırlık': 'weight',
        'Garanti Süresi': 'warranty_period',
        'Bağlantı Özellikleri': 'connectivity',
        'USB Sayısı': 'usb_ports',
        'Batarya Ömrü': 'battery_life',
        'Klavye': 'keyboard',
        'Touchpad': 'touchpad',
        'Kamera': 'camera',
        'Parmak İzi Okuyucu': 'fingerprint_reader',
        'Renk': 'color',
        'Menşei': 'country_of_origin',
        'Ürün Modeli': 'laptop_model',
        'Disk Kapasitesi (GB)': 'storage_capacity_gb',
        'Dokunmatik Ekran': 'touchscreen',
        'Klavye Aydınlatması': 'keyboard_backlight',
        'Şarj Girişi': 'charging_port',
        'Ürün Adı': 'product_name',
        'Hafıza Kapasitesi (GB)': 'ram_capacity_gb',
        'Type-C': 'type_c_port',
        'HDMI': 'hdmi',
        'Ses Çıkışı': 'audio_port',
        'Ön Kamera Çözünürlüğü': 'webcam_resolution',
        'Pil Gücü (mAh)': 'battery_capacity_mah',
        'Ekran Paneli': 'display_panel',
        'Bluetooth': 'bluetooth',
        'Wifi': 'wifi',
        'Hoparlör': 'speakers',
        'Kulaklık Girişi': 'headphone_jack',
        'Yenilenme Hızı': 'refresh_rate',
        'SSD Kapasitesi': 'ssd_capacity',
        'HDD Kapasitesi': 'hdd_capacity',
        'Ürün Tipi': 'product_type'
    }
    
    def rename_column(col_name):
        return column_translations.get(col_name, col_name)
    
    df = df.rename(columns=rename_column)
    df = df.fillna("")
    
    stats = {
        'total_execution_time': total_execution_time,
        'page_times': page_times,
        'product_count': product_count,
        'column_count': len(df.columns)
    }
    reporting.print_timing_statistics(stats)
    
    return df 