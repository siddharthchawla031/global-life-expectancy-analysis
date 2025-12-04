import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("../data/CleanedDataset.csv")

X = df.drop(columns=["Life_Expectancy"])
y = df["Life_Expectancy"]

model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X, y)

joblib.dump(model, "../results/life_expectancy_model.pkl")

# Save feature importance
fi = pd.DataFrame({"feature": X.columns, "importance": model.feature_importances_})
fi.to_csv("../results/feature_importance.csv", index=False)

print("Model trained and saved.")
