import cProfile
import pstats
import scraper

# Run the scraper with profiling
cProfile.run('scraper.main()', 'scraper_stats')

# Print the results
p = pstats.Stats('scraper_stats')
p.sort_stats('cumulative').print_stats(30)  # Show top 30 functions by cumulative time 