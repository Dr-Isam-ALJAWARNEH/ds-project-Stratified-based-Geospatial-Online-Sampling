# instructions
## follow the following instructions
-----------------------
<!-- Task 2 -->
# [ ] Task 2! 
# `Update: April 6, 2024`
### `N.B.` references are available in the end of this instruction file!
# `Required OPTIMIZATION ==> IMPORTANT!`
## `TODO:` 
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
    - check [S2 Region Coverer Online Viewer](https://igorgatis.github.io/ws2/), to see what it means by generating an S2 coverer!, You can also use the following [s2-geojson](https://github.com/pantrif/s2-geojson) as an S2 coverer viewer, and also read more about in the original work by google's [S2 geometry](http://s2geometry.io/) (`SIDE`: you can use those to write some parts of your paper!), also [S2 Covering Examples](http://s2geometry.io/devguide/examples/coverings.html)
    - probably you can use `s2sphere` framework to generate the coverer given a geohjson file. For example something similar to the following: [get a set of S2 cells covering a rectangle in](https://s2sphere.readthedocs.io/en/latest/quickstart.html)
    - here is the implementation of the [RegionCoverer class](https://s2sphere.readthedocs.io/en/latest/_modules/s2sphere/sphere.html#RegionCoverer) from s2shpere implementation!
- Do the same for geohash, generate geohash cover, then perform `filter-refine` spatial join, and compare (time-based and accuracy-based QoS requirements) with S2 and H3.
- read more about `filter-and-refine` spatial join in the following [presentation](https://isamaljawarneh.github.io/talks/FOSS4G2021.pdf)
    - also, a very good explanation (which you can use and cite when you write your paper) is our recent paper in [^1].
    - you specifically need to check the part that reads ```filter-and-refine algorithm [39]. It operates in three steps as follows....```
    
    [^1]: Al Jawarneh, I. M., Foschini, L., & Bellavista, P. (2023). Efficient Integration of Heterogeneous Mobility-Pollution Big Data for Joint Analytics at Scale with QoS Guarantees. Future Internet, 15(8), 263. [available online](https://www.mdpi.com/1999-5903/15/8/263)
--------------------
------------------
# [ ] Task 3! 
# `Update: April 6, 2024`
### `N.B.` references are available in the end of this instruction file!
# `Required OPTIMIZATION ==> IMPORTANT!`
## `TODO:` 
- Now, at this stage you should have already generated the geocodes (goehash, H3, S2) for point data (csv files) and the corresponding covering for each geocode (applied to geojson files), the next task that follows is the following:
- Develop an adapted version of the most famouse Density-based clustering algorithm DBSCAN!
# TODO `next`:
1. [ ] run the example clustering code (DBSCAN), attached in the new folder "DBSCAN_Clustering" inside 'starting_code' folder
2. [ ] read more about how DBSCAN works in scikit-learn
    > [DBSCAN scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
3. [ ] you need to use ```Silhouette Coefficient ```for evaluation
    > ***"If the ground truth labels are not known, evaluation can only be performed using the model results itself. In that case, the Silhouette Coefficient comes in handy."***
    an example is here:
    [Demo of DBSCAN clustering algorithm](https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py)
- Then you need to `adapt` the stock version of the DBSCAN so that it operates a bit differently, specifically you need to do the following:
    - plain scikit-learn DBSCAN distance calculation relies on using  ```haversine``` as a distance metric to calculate haversine distances (i.e., geometrical distances) between coordinates (longitudes/latitudes pairs)
  > the attention that should be given in this case is that you did not capture any statistics regarding the distribution of the pm25 values (our target variable), you could for example capture the histograms of those values.
  Read more about possible values of ```pm2.5``` in this reference [PM2.5 particles in the air](https://www.epa.vic.gov.au/for-community/environmental-information/air-quality/pm25-particles-in-the-air). This means that you need to create a histogram showing the density of each bracket, your binning strategy should rely on the community definition of ranges of values. For example, binning example is the follwoing: Less than 25, 25–50, 50–100, 100–300, More than 300. 
    - Also, draw histograms showing the same binning and density of pm2.5 values in each neighborhood in your data. By the way, how many neighborhoods you have in your data?!
  > this is important as it will inform us about the fact whether nearby locations are having similar pm25 values. Why do we need to do this, because it is only in that case we consider those as a cluster, since they are geographiclly nearby, and also having simialr feature values (pm25 in this case). So what you need to do next is the following:
  - .. ```Extract and normalize several features```, similar to what has been done in the following tutorial, read specifically [Extending DBSCAN beyond just spatial coordinates](https://musa-550-fall-2020.github.io/slides/lecture-11A.html), thereafter ```Run DBSCAN to extract high-density clusters``` passing as an argument to the DBSCAN the new ```scaled features```, probably something like ```cores, labels = dbscan(features, eps=eps, min_samples=min_samples)``` . notice passing features (including pm25, longitude, latitude) instead of simply the coordinates.
  - having done this novel distance calculation (based on geometrical distance and pm25 values distance), calculate again the ```silhouette_score```, and check wether you obtain a higher accuracy (higher silhouette_score values) or not!

  > **N.B.** we are able to do this because of the definition of ```metric``` in DBSCAN which says **metric: The metric to use when calculating distance between instances in** a ```feature array``` so, it  a distance between several features is possible, given a ```feature array```, so put your scaled features in a feature array.
- `THEREAFTER`! You need to create a novel `adapted` version of DBSCAN that is based on the following: 
    - first, the stock version of DBSCAN depends on two main parameters (`epsilon`==> `The maximum distance between two samples for one to be considered as in the neighborhood of the other` and `min_samples` ==> `The number of samples (or total weight) in a neighborhood for a point to be considered as a core point.`). perhaps most importantly is that DBSCAN is an iterative algorithm that needs to fine `core` points (i.e., `cluster centers`) and calculate `distances` (could be `haversine`, `manhattan`, `euclidean`, etc., see the sklearn documentation for further details!, [sklearn.metrics.pairwise_distances](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html)). `however!`, those calculations are computationally expensive when we have big geospatial data (it is a geometric calculation, and geometry is expensive!). So, you need to `minimize` those calculations. But how?!!!
        - If you think about the geocodes that you have generated (being that `S2`, `H3` or `geohash`) where each geocode contains within its premises a set of points (i.e., set long/lat pairs). Think of those geocodes as Minimum Bounding Rectangles (MBR), or Minimum Bounding Boxes (MBB). Having said that, we have already built successfully aa pre-filtering stage! That is to say, those geocodes are prefilters. Then theoritically speaking, points belonging to same geocode (i.e., are within the MBR represented by the geocode) belong to the same cluster even without applying DBSCAN! that is a cheap quick-and-approximate filter!. So, referring back to the parameters, `min_samples`, we simply count the number of points in each geocode (being that `S2`, `H3` or `geohash`), if that count is greater than `min_samples`, we consider this geocode as a cluster (term this `geocode cluster` hereafter for clarity) without having to calculate any distances! (cheap filter), then we pass only the points (call those as `outliers` for reference hereafter) that belong to geocodes that are having points less than the threshold `min_samples` to the plain DBSCAN to find the remaining clusters by appling the expensive distance calculations in DBSCAN. However, we should do this with caveat! as some of those points are geographically close in distance to some of the `geocode cluster` clusters that resulted in the filtering step!, what does this mean. This means that before generating new clusters based on some of those `outlier` points, we need to check whether their distances to some `geocode cluster` cores are less than the threshold `epsilon`, if so the case then they belong to one or more `geocode cluster` clusters, otherwise we pass them to the plain version of the DBSCAN. This is just a propsed algorithm and you are expected to develop it further as per your comprehension of the DBSCAN and its implementation in scikit-learn.
    - You then need to compare this algorithm with the stock version of DBSCAN as implemented in the scikit-learn. You need to capture two metrics: running time of each algorithm and the accuracy metric (for example, use `silhouette_score` from scikit-learn) [**bonus** if you could apply [geosilhouettes](https://pysal.org/esda/notebooks/geosilhouettes.html)]
see `appendix-A` for further related instructions! 

--------------
------------------
-----------------
--------------------------
# [ ] Task1
1. [X] run the example starting code and familiarize yourself with some geosaptial processing techniques, including:
    - sampling
    - spatial join
    - geo-visualization

2. [ ] reference papers include:
    # Category A : for sampling desing and Approximate Query Processing (AQP)
    > Spatial-aware approximate big data stream processing [^2] and
    > Polygon Simplification for the Efficient Approximate Analytics of Georeferenced Big Data[^3]
    # Category B: for spatial join procesing
    > SpatialSSJP: QoS-Aware Adaptive Approximate Stream-Static Spatial Join Processor [^6]
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
[^2]: Al Jawarneh, I. M., Bellavista, P., Foschini, L., & Montanari, R. (2019, December). Spatial-aware approximate big data stream processing. In 2019 IEEE global communications conference (GLOBECOM) (pp. 1-6). IEEE. [available online](https://www.researchgate.net/profile/Isam-Al-Jawarneh/publication/339562314_Spatial-Aware_Approximate_Big_Data_Stream_Processing/links/5ff45764299bf14088708888/Spatial-Aware-Approximate-Big-Data-Stream-Processing.pdf)
[^3]: Al Jawarneh, I. M., Foschini, L., & Bellavista, P. (2023). Polygon Simplification for the Efficient Approximate Analytics of Georeferenced Big Data. Sensors, 23(19), 8178.[available online](https://www.mdpi.com/1424-8220/23/19/8178)
[^6]: Al Jawarneh, I. M., Bellavista, P., Corradi, A., Foschini, L., & Montanari, R. (2023). SpatialSSJP: QoS-Aware Adaptive Approximate Stream-Static Spatial Join Processor. IEEE Transactions on Parallel and Distributed Systems. [available online](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10309986)

-------------------

NEW! 31 March 2024
- Generate a covering geocode (geohash, H3, S2) for all the polygons in the geojson file. What does this mean, you can think of a geocode as a Minimum Bounding Rectangle (MBR), then each administrative division (neighborhood, district, etc) in the city can be covered by few MBRs, those represent the geocodes (H3, S2, geohash) that cover completely the administrartive polygon. After this, to perform the join (apart from the stock version of Geopandas which applies sjoin), you can mimic the design of the filter-and-refinement approach. The filter is simply an equi-join between the geocode cover and the geocodes of the points from the CSV file, the result is a set of candidates, then the filter is an application of the ray-casting algorithm, where you check those that in real geometries are within a neighborhood by using the costly geometrical operation. We can discuss this concept in a meeting!

- For the paper writing and submission
- consider one of the following two conference
    - [MCNA - Spain](https://mcna-conference.org/2024/committee.php)
    - [IDSTA - Croatia](https://idsta-conference.org/2024/calls.php)
===============================
-----------------------
# `Appendices`
1) `appendix-A` one importance configurable parameter in this case is the distance metric.
  > you can use instead 
    - most importantly the following : ```From scikit-learn: [‘cityblock’, ‘euclidean’, ‘l1’, ‘l2’, ‘manhattan’].``` [sklearn.metrics.pairwise_distances](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html)
    - and probably aome of the following ```From scipy.spatial.distance: [‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘dice’, ‘hamming’, ‘jaccard’, ‘kulsinski’, ‘rogerstanimoto’, ‘russellrao’,, ‘sokalmichener’, ‘sokalsneath’, ```

  - then, having permutate this configurable parameter, capture the ```silhouette_score``` and compare, then draw an x-y figure such as the following [figure attached in notebook], (```you can do those graphs in MS excel after capturing the numbers```):
  - Provide a detailed explanation of the values you obtained for ```Silhouette Coefficient```
    - take some insights from [scikit-learn docs](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html#sklearn.metrics.silhouette_score)
    - That is to say, >
    > "The best value is 1 and the worst value is -1. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar."
  - you need to do more analytics and Exploratory Spatio-Temporal Data Analytics (ESTDA,  read specifically [Extending DBSCAN beyond just spatial coordinates](https://musa-550-fall-2020.github.io/slides/lecture-11A.html), thereafter, for example ```Identify the 5 largest clusters``` , ```Get mean statistics for the top 5 largest clusters```, ```Visualize the top 5 largest clusters```, ```Visualizing one cluster at a time```.
- add other metrics from the [sklearn.metrics](https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation), for example the following:
  > - ```Davies-Bouldin Index```, **Zero is the lowest possible score. Values closer to zero indicate a better partition.**
  for your experiment, we have obtained a number on par with 2.78!, which is very high! so probably your clustering scheme misses something! try different combinations of configurations (sampling scheme, distance methods, distance based on combination of features such as geographical long/lat and pm25 values), read my previous comments to get insights.
    - ```Calinski-Harabasz Index```. You have computed that already, but what is your explanation and reasoning of the results obtained!