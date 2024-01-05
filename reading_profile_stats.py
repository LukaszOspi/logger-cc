import pstats

# Load the statistics from the file
p = pstats.Stats('profile_stats')

# Sort the statistics by cumulative time spent and print the top entries
p.sort_stats('cumulative').print_stats(110)

# Alternatively, sort by internal time and print the top entries
p.sort_stats('time').print_stats(110)

# You can also print stats for specific functions
# p.print_stats('your_function_name')