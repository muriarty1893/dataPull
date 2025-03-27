"""
Utilities module for the scraper.
Contains helper functions.
"""

import os
import pandas as pd
import time
import cProfile
import pstats
from scraper_project.scraper import reporting
from scraper_project.scraper.config import settings

def save_to_csv(df, file_path=None):
    """
    Save a DataFrame to a CSV file.
    
    Args:
        df: pandas.DataFrame to save
        file_path: Path to save the file to. If None, uses the default path from settings.
    """
    if file_path is None:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'output')
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, settings.OUTPUT_FILE)
    
    df.to_csv(file_path, encoding=settings.OUTPUT_ENCODING)
    reporting.print_save_confirmation(file_path)

def profile_scraper(func, output_file='scraper_stats'):
    """
    Profile a function and print the results.
    
    Args:
        func: Function to profile
        output_file: File to save profiling results to
    """
    cProfile.run(f'{func.__name__}()', output_file)
    p = pstats.Stats(output_file)
    p.sort_stats('cumulative').print_stats(30)  # Show top 30 functions by cumulative time

def time_execution(func):
    """
    Decorator to time the execution of a function.
    
    Args:
        func: Function to time
    
    Returns:
        Wrapped function that prints execution time
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper 