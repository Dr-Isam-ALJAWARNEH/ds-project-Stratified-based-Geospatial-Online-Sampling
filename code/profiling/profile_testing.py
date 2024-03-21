import pandas as pd
from numpy import arange as np_arange


TRIPS_PATH = "../../data/NYC_Pilot2_PM_Part1.csv"

trips = pd.read_csv(TRIPS_PATH)
trips = trips[
    (trips['latitude']  != 0) &
    (trips['longitude'] != 0)
]

for sampling_fraction in np_arange(0.1, 1.1, 0.1):
    sampled_trips = trips.sample(frac=sampling_fraction)
    print("Number of rows for sampling fraction %.1f: %d / %d" % (sampling_fraction, sampled_trips.shape[0], trips.shape[0]))
