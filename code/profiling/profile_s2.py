import pandas as pd
from s2 import s2
from timeit import repeat as timeit_repeat
from numpy import arange as np_arange


s2_resolution = 14


def group_by_s2(df):
    df['s2'] = df.apply(lambda x: s2.geo_to_s2(x.latitude, x.longitude, s2_resolution), axis=1)
    return df.groupby('s2')


TRIPS_PATH = "../../data/NYC_Pilot2_PM_Part1.csv"

trips = pd.read_csv(TRIPS_PATH)
trips = trips[
    (trips['latitude']  != 0) &
    (trips['longitude'] != 0)
]

for sampling_fraction in np_arange(0.1, 1.1, 0.1):
    sampled_trips = trips.sample(frac=sampling_fraction)
    print("Best of 5 runs for sampling fraction %.1f:" % sampling_fraction, min(timeit_repeat(
        "group_by_s2(sampled_trips)",
        setup="from __main__ import group_by_s2, sampled_trips",
        repeat=5, number=1
    )))
