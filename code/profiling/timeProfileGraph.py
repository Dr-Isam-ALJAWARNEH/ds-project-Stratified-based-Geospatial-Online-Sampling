import matplotlib.pyplot as plt

# Sample data for three algorithms' running times
geohash_times = [
    0.3018713000000002,
    0.600444,
    0.9058516000000001,
    1.217835899999999,
    1.5222499999999997,
    1.855830400000002,
    2.1203740000000053,
    2.428716299999998,
    2.7795766000000057,
    3.089560899999995
]  
H3_times = [
    0.19227039999999995,
    0.3902357999999997,
    0.5944172000000005,
    0.7765814999999998,
    0.9839281999999994,
    1.1767145999999986,
    1.3942932,
    1.5624377000000038,
    1.7527727999999954,
    1.7527727999999954
]  
S2_times = [
    0.4644881999999999,
    0.9421867000000006,
    1.4043713999999987,
    1.8964394999999996,
    2.3502612999999997,
    2.8036381999999946,
    3.2955156999999957,
    3.769479199999992,
    4.253074499999997,
    4.711142800000005
]  

# Sample sizes as percentages
sample_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Plotting the bar graph
bar_width = 0.25  # Width of each bar
index = range(len(sample_sizes))  # X-axis index for bars

# Plotting bars for each algorithm
plt.bar(index, H3_times, width=bar_width, label='H3')
plt.bar([i + bar_width for i in index], geohash_times, width=bar_width, label='Geohash')
plt.bar([i + 2 * bar_width for i in index], S2_times, width=bar_width, label='S2')

# Adding labels and title
plt.xlabel('Sample Sizes (%)')
plt.ylabel('Running Time')
plt.title('Comparison of Algorithms Running Time')
plt.xticks([i + bar_width for i in index], sample_sizes)
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
