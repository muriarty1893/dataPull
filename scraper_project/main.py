import argparse
from scraper_project.scraper.core import scrape
from scraper_project.scraper.utils import save_to_csv, profile_scraper, time_execution
from scraper_project.scraper.config import settings

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape product data from Trendyol')
    
    parser.add_argument('--start-page', type=int, default=settings.START_PAGE, help=f'Starting page number (default: {settings.START_PAGE})')
    
    parser.add_argument('--end-page', type=int, default=settings.END_PAGE, help=f'Ending page number (default: {settings.END_PAGE})')
    
    parser.add_argument('--output', type=str, default=None, help=f'Output file path (default: output/{settings.OUTPUT_FILE})')
    
    parser.add_argument('--profile', action='store_true', help='Run with profiling enabled')
    
    return parser.parse_args()

def update_settings(args):
    settings.START_PAGE = args.start_page
    settings.END_PAGE = args.end_page

@time_execution
def main():
    args = parse_arguments()
    update_settings(args)
    
    if args.profile:
        profile_scraper(scrape)
    else:
        df = scrape()
        
        save_to_csv(df, args.output)
    
    return 0

if __name__ == "__main__":
    main() 