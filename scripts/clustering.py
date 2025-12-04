import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv("../data/CleanedDataset.csv")

# Select top features for clustering
cols = [
    "Life_Expectancy", "Infant_Mortality_Rate", "Maternal_Mortality_Ratio",
    "GDP_per_Capita", "Birth_Rate", "Death_Rate"
]

X = df[cols].copy()
X = X.dropna()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
df["Cluster"] = kmeans.fit_predict(X_scaled)

cluster_summary = df.groupby("Cluster")[cols].mean()
cluster_summary.to_csv("../results/cluster_summary.csv")

df.to_csv("../results/clustered_data.csv", index=False)

print("Clustering completed.")
