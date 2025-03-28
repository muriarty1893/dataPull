import os
import pandas as pd
import time
from scraper_project.scraper import reporting
from scraper_project.scraper.config import settings

def save_to_csv(df, file_path=None):
    if file_path is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'output')
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, settings.OUTPUT_FILE)
    
    df.to_csv(file_path, encoding=settings.OUTPUT_ENCODING)
    reporting.print_save_confirmation(file_path) 