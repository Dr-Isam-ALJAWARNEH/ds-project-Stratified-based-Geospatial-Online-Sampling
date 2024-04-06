# instructions
## follow the following instructions
-----------------------
# `Update: April 4, 2024`
### `N.B.` references are available in the end of this instruction file!
## `TODO:` 
> [!IMPORTANT]
- create a covering h3 for each polygon in the `geojson` file, the result is an array of H3 values covering each polygon,
for example , given a polygon ``` python 
coordinates: [[
      [-122.47485823276713, 37.85878356045377],
      [-122.47504834087829, 37.86196795698972],
      [-122.47845104316997, 37.86010614563313],
      [-122.47485823276713, 37.85878356045377]
    ]]```, applying
```const hexagons = geojson2h3.featureToH3Set(polygon, 10);```
this will result in an array, `// -> ['8a2830855047fff', '8a2830855077fff', '8a283085505ffff', '8a283085506ffff']`, for each polygon in the geojson the same appllies, an array of covering H3 values.
> you can get insights from here, [geojson2h3](https://github.com/uber/geojson2h3)
- we need to create a compact representation, specifically you need to  `explode` the arrays so that you have two columns, one column is `neighborhood` and the other is the `h3 value`, such that for each neighborhood we have several corresponding h3 values (those are the values appeared previously in the array).

    | neighborhood    | H3 |
    | -------- | ------- |
    | Bronx  | '8a2830855047fff'    |
    | Bronx | '8a2830855077fff'     |
    | Bronx    | '8a283085505ffff'    |
    | center  | '8a283085506ffff'    |
    | center | '8a283085504ffff'     |
    | center    | '8a283085502ffff'    |

> you can imagine then that one can perform a filter-refine spatial join (between a csv and geojson files) as  follows: 
- perform the equi-join first on the H3 values, such that you find neighborhood to which each long/lat pair represented by H3 from the csv (mobility, air quality data etc.,) belongs to. Same H3 values can have several neighborhoods because this is an approximate join known as MBR-join (MBR for Minimum Bounding Rectangle), this is a kind of equi-join. This will result in candidates for which you have to apply the exact geometrical operation to check whether a point (long/lat pair represented by H3 value) falls within the neighborhood (i.e., the polygon in the geojson file) or not in real geometries, which is normally achieved using ray-casting algorithm.
- Having generated the `H3 cover` from the polygon file, you develop a simple algorithm to resemble the filter-and-refinement join using the H3 as the encoding system. 
- Do the same for Google's S2, generate a cover for each polygon in the geojson file, the result should be a dataframe with a compact format (two columns, `neighborhood ` and `S2 value`), same as described for the H3. 
    - also implement a filter-and-refine spatial join using S2 this time.
- Do the same for geohash, generate geohash cover, then perform `filter-refine` spatial join, and compare (time-based and accuracy-based QoS requirements) with S2 and H3.
- read more about `filter-and-refine` spatial join in the following [presentation](https://isamaljawarneh.github.io/talks/FOSS4G2021.pdf)
    - also, a very good explanation (which you can use and cite when you write your paper) is our recent paper in [^1].
    
    [^1]: Al Jawarneh, I. M., Foschini, L., & Bellavista, P. (2023). Efficient Integration of Heterogeneous Mobility-Pollution Big Data for Joint Analytics at Scale with QoS Guarantees. Future Internet, 15(8), 263. [available online](https://www.mdpi.com/1999-5903/15/8/263)
--------------------
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

- For the paper writing and submission
- consider one of the following two conference
    - [MCNA - Spain](https://mcna-conference.org/2024/committee.php)
    - [IDSTA - Croatia](https://idsta-conference.org/2024/calls.php)