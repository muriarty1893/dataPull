BASE_URL = "https://www.trendyol.com/laptop-x-c103108?pi="
START_PAGE = 1
END_PAGE = 1  # Reduced to 1 page for faster scraping
DEBUG = True

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Minimum delay ayarları
MIN_DELAY = 0.01  # Minimum delay
MAX_DELAY = 0.02  # Maximum delay

# Enable parallel processing
USE_PARALLEL = True
MAX_WORKERS = 5  # Paralel işlem sayısını artırdık

# Data saving settings
SAVE_INTERVAL = 10  # Save data every 10 products
BACKUP_FILE = "data_backup.csv"  # Backup file for periodic saves
AUTO_RECOVERY = True  # Enable auto recovery from last saved point

OUTPUT_FILE = "data.csv"
OUTPUT_ENCODING = "utf-8"

PRODUCT_WRAPPER_CLASS = "p-card-wrppr"
PRODUCT_CARD_BORDER_CLASS = "p-card-chldrn-cntnr"
PRODUCT_DESC_CLASS = "prdct-desc-cntnr"
PRODUCT_NAME_CLASS = "prdct-desc-cntnr-name hasRatings"
PRICE_DISCOUNTED_CLASS = "prc-box-dscntd"
PRICE_SELLING_CLASS = "prc-box-sllng"
SPECIFICATIONS_CONTAINER_CLASS = "detail-attr-container"
SPECIFICATION_ITEM_CLASS = "detail-attr-item"
PRODUCT_FEATURES_CLASS = "product-features"
FEATURE_CLASS = "product-feature"
FEATURE_NAME_CLASS = "feature-name"
FEATURE_VALUE_CLASS = "feature-value"   
PRODUCT_DESCRIPTION_CLASS = "product-description" 