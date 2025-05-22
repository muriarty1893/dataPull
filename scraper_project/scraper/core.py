import time
import random
import requests
import pandas as pd
import os
from scraper_project.scraper.config import settings
from scraper_project.scraper import reporting
from scraper_project.scraper import parser

def save_backup(data, backup_file):
    if not data:
        return
    
    df = pd.DataFrame(data)
    df.to_csv(backup_file, encoding=settings.OUTPUT_ENCODING, index=False)
    if settings.DEBUG:
        print(f"Backup saved to {backup_file}")

def load_backup(backup_file):
    if os.path.exists(backup_file):
        try:
            return pd.read_csv(backup_file, encoding=settings.OUTPUT_ENCODING).to_dict('records')
        except Exception as e:
            if settings.DEBUG:
                print(f"Error loading backup: {e}")
    return []

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
    
    # Load backup if exists and auto recovery is enabled
    if settings.AUTO_RECOVERY:
        backup_data = load_backup(settings.BACKUP_FILE)
        if backup_data:
            all_data.extend(backup_data)
            product_count = len(backup_data)
            if settings.DEBUG:
                print(f"Recovered {product_count} products from backup")
    
    for page_number in range(settings.START_PAGE, settings.END_PAGE + 1):
        page_data, page_time, products_on_page = scrape_page(page_number)
        
        if page_data:
            all_data.extend(page_data)
            page_times.append(page_time)
            product_count += products_on_page
            
            # Save backup periodically
            if product_count % settings.SAVE_INTERVAL == 0:
                save_backup(all_data, settings.BACKUP_FILE)
    
    total_execution_time = time.time() - start_time_total
    
    df = pd.DataFrame(all_data)
    
    if 'originalPrice' in df.columns:
        df = df.drop('originalPrice', axis=1)
    
    # Save final backup
    save_backup(all_data, settings.BACKUP_FILE)
    
    column_translations = {
        'link': 'link',
        'brand': 'brand',
        'product': 'product',
        'Price': 'price',
        
        'Garanti Tipi': 'warranty',
        'İşletim Sistemi': 'os',
        'İşlemci Tipi': 'processor',
        'İşlemci Nesli': 'cpugen',
        'RAM': 'ram',
        'Disk Kapasitesi': 'storage',
        'Disk Türü': 'disktype',
        'Ekran Boyutu': 'screensize',
        'Çözünürlük': 'resolution',
        'Ekran Kartı': 'gpu',
        'Ekran Kartı Hafızası': 'gpumemory',
        'Ağırlık': 'weight',
        'Garanti Süresi': 'warrantyperiod',
        'Bağlantı Özellikleri': 'connectivity',
        'USB Sayısı': 'usbports',
        'Batarya Ömrü': 'battery',
        'Klavye': 'keyboard',
        'Touchpad': 'touchpad',
        'Kamera': 'camera',
        'Parmak İzi Okuyucu': 'fingerprint',
        'Renk': 'color',
        'Menşei': 'origin',
        'Ürün Modeli': 'model',
        'Disk Kapasitesi (GB)': 'storagegb',
        'Dokunmatik Ekran': 'touchscreen',
        'Klavye Aydınlatması': 'keyboardlight',
        'Şarj Girişi': 'chargingport',
        'Ürün Adı': 'productname',
        'Hafıza Kapasitesi (GB)': 'ramgb',
        'Type-C': 'typec',
        'HDMI': 'hdmi',
        'Ses Çıkışı': 'audio',
        'Ön Kamera Çözünürlüğü': 'webcam',
        'Pil Gücü (mAh)': 'batterycapacity',
        'Ekran Paneli': 'panel',
        'Bluetooth': 'bluetooth',
        'Wifi': 'wifi',
        'Hoparlör': 'speakers',
        'Kulaklık Girişi': 'headphonejack',
        'Yenilenme Hızı': 'refreshrate',
        'SSD Kapasitesi': 'ssd',
        'HDD Kapasitesi': 'hdd',
        'Ürün Tipi': 'producttype'
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