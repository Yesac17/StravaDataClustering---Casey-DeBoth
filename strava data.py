import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv(
    'activities.csv',
                 thousands=',',
                 parse_dates=["Activity Date"],
                 date_format="%b %d, %Y, %I:%M:%S %p"
                 )

df['Distance'] = pd.to_numeric(df['Distance'])
df['Moving Time'] = pd.to_numeric(df['Moving Time'])
df['Average Heart Rate'] = pd.to_numeric(df['Average Heart Rate'])
df['Elevation Gain'] = pd.to_numeric(df['Elevation Gain'])
df = df[df['Activity Type'] == 'Run']

cutoff = pd.Timestamp.today() - pd.DateOffset(years=4)
df_recent = df.loc[df["Activity Date"] >= cutoff].copy()

data = df_recent[[
    'Activity Date','Activity Name',
    'Distance','Average Speed',
    'Average Heart Rate','Max Speed','Max Heart Rate','Idle Time','Moving Time', 'Relative Effort'
]].dropna()

# Split labels vs. features (they’ll be the same length)
labels = data[['Activity Date','Activity Name']].copy()
features = data[[
    'Distance','Average Speed',
    'Average Heart Rate','Max Speed','Max Heart Rate','Idle Time','Moving Time', 'Relative Effort'
]].astype(float)

# Standardize & cluster
X = features.to_numpy()
std = np.std(X, axis=0)
X_scaled = X / std

# Elbow plot
inertia = []
ks = range(1, 11)
for k in ks:
    km = KMeans(n_clusters=k, n_init=20).fit(X_scaled)
    inertia.append(km.inertia_)

plt.plot(ks, inertia, 'o-')
plt.xlabel('k clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

# Fit KMeans with chosen k = 3
k = 6
km = KMeans(n_clusters=k, n_init=20).fit(X_scaled)
labels['Cluster'] = km.labels_


generic = {
    "morning run",
    "afternoon run",
    "evening run",
    "lunch run"
}

is_non_generic = ~labels['Activity Name'] \
                    .str.strip() \
                    .str.lower() \
                    .isin(generic)

# Rescale and print cluster centers + members
centers = km.cluster_centers_ * std
centers_df = pd.DataFrame(centers, columns=features.columns)
centers_df.index.name = 'Cluster'
print("Cluster centers (original units):")
print(centers_df, '\n')

labels_filtered = labels[is_non_generic]

for cluster in range(k):
    print(f"=== Cluster {cluster} ({len(labels[labels['Cluster']==cluster])} runs) ===")
    subset = labels[labels['Cluster'] == cluster]
    # print date + name for each run in this cluster
    # for _, row in subset.iterrows():
    #     print(f"{row['Activity Date']}: {row['Activity Name']}")
    # print()


for cluster in range(k):
    subset = labels_filtered[labels_filtered['Cluster'] == cluster]
    print(f"=== Cluster {cluster} ({len(subset)} non‑generic runs) ===")
    for _, row in subset.iterrows():
        print(f"{row['Activity Date']}: {row['Activity Name']}")
    print()