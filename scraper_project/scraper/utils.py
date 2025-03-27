import os
import pandas as pd
import time
import cProfile
import pstats
from scraper_project.scraper import reporting
from scraper_project.scraper.config import settings

def save_to_csv(df, file_path=None):
    if file_path is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'output')
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, settings.OUTPUT_FILE)
    
    df.to_csv(file_path, encoding=settings.OUTPUT_ENCODING)
    reporting.print_save_confirmation(file_path)

def profile_scraper(func, output_file='scraper_stats'):
    cProfile.run(f'{func.__name__}()', output_file)
    p = pstats.Stats(output_file)
    p.sort_stats('cumulative').print_stats(30)

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper 