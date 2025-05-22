import argparse
import os
from scraper_project.scraper.core import scrape
from scraper_project.scraper.reporting import save_to_csv
from scraper_project.scraper.config import settings

def parse_arguments():
    parser = argparse.ArgumentParser(description='Trendyol laptop verilerini çek')
    parser.add_argument('--start', type=int, required=True, help='Başlangıç sayfa numarası')
    parser.add_argument('--end', type=int, required=True, help='Bitiş sayfa numarası')
    parser.add_argument('--debug', action='store_true', help='Debug bilgilerini göster')
    
    return parser.parse_args()

def update_settings(args):
    settings.START_PAGE = args.start
    settings.END_PAGE = args.end
    settings.DEBUG = args.debug
    
    # Dinamik dosya isimleri oluştur
    settings.OUTPUT_FILE = f"data_{args.start}_{args.end}.csv"
    settings.BACKUP_FILE = f"data_backup_{args.start}_{args.end}.csv"

def main():
    args = parse_arguments()
    update_settings(args)
    
    print(f"Laptop verileri çekiliyor: {settings.BASE_URL}{settings.START_PAGE} - {settings.END_PAGE}")
    print(f"Çıktı dosyası: {settings.OUTPUT_FILE}")
    print(f"Yedek dosyası: {settings.BACKUP_FILE}")
    
    # Çıktı klasörünü oluştur
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Tam dosya yollarını ayarla
    settings.OUTPUT_FILE = os.path.join(output_dir, settings.OUTPUT_FILE)
    settings.BACKUP_FILE = os.path.join(output_dir, settings.BACKUP_FILE)
    
    df = scrape()
    save_to_csv(df, settings.OUTPUT_FILE)
    
    return 0

if __name__ == "__main__":
    main() 