import pandas as pd
import joblib

model = joblib.load("../results/life_expectancy_model.pkl")
df = pd.read_csv("../data/CleanedDataset.csv")

def predict(country, year):
    row = df[(df["Country"] == country) & (df["Year"] == year)]
    if row.empty:
        return None
    X = row.drop(columns=["Life_Expectancy"])
    return model.predict(X)[0]

if __name__ == "__main__":
    results = []
    for country in ["India", "China", "Sri Lanka"]:
        for yr in [2025, 2030]:
            pred = predict(country, 2019)  # Last available features
            results.append([country, yr, pred])

    out = pd.DataFrame(results, columns=["Country", "Year", "Predicted_Life_Expectancy"])
    out.to_csv("../results/future_predictions.csv", index=False)
    print("Predictions saved.")
