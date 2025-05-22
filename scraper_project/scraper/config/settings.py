BASE_URL = "https://www.trendyol.com/laptop-x-c103108?pi="
DEBUG = True

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Minimum delay ayarları
MIN_DELAY = 0.01
MAX_DELAY = 0.02

# Enable parallel processing
USE_PARALLEL = True
MAX_WORKERS = 5

# Data saving settings
SAVE_INTERVAL = 10  # Her 10 sayfada bir kaydet
AUTO_RECOVERY = True

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