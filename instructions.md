# instructions
## follow the following instructions
1. [ ] run the example starting code and familiarize yourself with some geosaptial processing techniques, including:
    - sampling
    - spatial join
    - geo-visualization

2. [ ] reference papers include:
    > [1. online spatial sampling](https://www.researchgate.net/profile/Isam-Al-Jawarneh/publication/339562314_Spatial-Aware_Approximate_Big_Data_Stream_Processing/links/5ff45764299bf14088708888/Spatial-Aware-Approximate-Big-Data-Stream-Processing.pdf) and
    > [2. AQP](https://www.mdpi.com/1999-5903/15/8/263)
    > [3. AQP](https://www.mdpi.com/1424-8220/21/12/4160)
In those papers, geohash encoding have been used for sampling, your task is to use ```Google's S2``` and ```Uber's H3``` for encoding, and build a sampler based on those and then compare the accuracy and time-based QoS constraints!
3. [ ] search appropriate open source implementations for those algorithms in Python!, for example:
    > [S2 Python](https://pypi.org/project/s2/)
    > [s2 RegionCoverer](https://github.com/pantrif/s2-geojson)
    > [geojson to H3](https://github.com/uber/geojson2h3)
    > [H3 grid](https://geographicdata.science/book/data/h3_grid/build_sd_h3_grid.html)
    >[H3](https://h3geo.org/docs/api/regions/)
    >[H3-geojson](https://github.com/kapil-grv/H3-geojson)

also interesting:
- [How to create a Choropleth map using Uber H3, Plotly & Python](https://medium.com/analytics-vidhya/how-to-create-a-choropleth-map-using-uber-h3-plotly-python-458f51593548)

- [Uber H3 for Data Analysis with Python](https://towardsdatascience.com/uber-h3-for-data-analysis-with-python-1e54acdcc908)
-------------------

NEW! 31 March 2024
- Generate a covering geocode (geohash, H3, S2) for all the polygons in the geojson file. What does this mean, you can think of a geocode as a Minimum Bounding Rectangle (MBR), then each administrative division (neighborhood, district, etc) in the city can be covered by few MBRs, those represent the geocodes (H3, S2, geohash) that cover completely the administrartive polygon. After this, to perform the join (apart from the stock version of Geopandas which applies sjoin), you can mimic the design of the filter-and-refinement approach. The filter is simply an equi-join between the geocode cover and the geocodes of the points from the CSV file, the result is a set of candidates, then the filter is an application of the ray-casting algorithm, where you check those that in real geometries are within a neighborhood by using the costly geometrical operation. We can discuss this concept in a meeting!