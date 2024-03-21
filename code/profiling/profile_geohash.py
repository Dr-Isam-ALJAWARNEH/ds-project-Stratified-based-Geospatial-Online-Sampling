import pandas as pd
import pygeohash as gh
from timeit import repeat as timeit_repeat
from numpy import arange as np_arange


geohash_precision = 6


def group_by_geohash(df):
    df['geohash'] = df.apply(lambda x: gh.encode(x.latitude, x.longitude, precision=geohash_precision), axis=1)
    return df.groupby('geohash')


TRIPS_PATH = "../../data/NYC_Pilot2_PM_Part1.csv"

trips = pd.read_csv(TRIPS_PATH)
trips = trips[
    (trips['latitude']  != 0) &
    (trips['longitude'] != 0)
]

for sampling_fraction in np_arange(0.1, 1.1, 0.1):
    sampled_trips = trips.sample(frac=sampling_fraction)
    print("Best of 5 runs for sampling fraction %.1f:" % sampling_fraction, min(timeit_repeat(
        "group_by_geohash(sampled_trips)",
        setup="from __main__ import group_by_geohash, sampled_trips",
        repeat=5, number=1
    )))
