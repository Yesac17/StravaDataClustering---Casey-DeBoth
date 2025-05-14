# Strava Run Clustering

In this project I am using my Strava data with K‑Means clustering to see if I can automatically group similar runs.

---

## Project Overview

1. **Data Cleanup**  
   - Load `activities.csv`.  
   - Filter only runs from the last 4 years.

2. **Feature Assembly**  
   - Keep per‑run summary stats:  
     ```
     Distance, Average Speed, Average Heart Rate,
     Max Speed, Max Heart Rate, Idle Time,
     Moving Time, Relative Effort
     ```
   - Drop any rows with missing values.

3. **Scaling**  
   - Compute standard deviation on the dataset for each feature.  
   - Divide all features by their stds.

4. **Elbow Method**  
   - Run K‑Means for k = 1…10, record `inertia_` (within‑cluster sum of squares).  
   - Plot inertia vs k to eyeball where the curve “elbows.”

5. **Cluster Assignment**  
   - Choose k = 6.  
   - Fit final K‑Means and tag each run with its cluster label.

6. **Post‑processing**  
   - Define a small set of “generic” run names (`morning run`, `afternoon run`, etc.) and filter them out so we focus on unique run titles.  
   - List the date + name of each non‑generic run in each cluster for quick inspection.
