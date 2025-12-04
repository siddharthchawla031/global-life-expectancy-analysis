import pandas as pd

def load_and_clean(path="../data/UnifiedDataset.csv"):

    df = pd.read_csv(path)

    # Standardize columns
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("[^0-9a-zA-Z_]+", "", regex=True)

    # Drop columns with >50% missing
    missing_percent = df.isnull().mean()
    cols_to_drop = missing_percent[missing_percent > 0.5].index
    df = df.drop(columns=cols_to_drop)

    # Convert numeric columns
    numeric_cols = df.columns[df.dtypes != "object"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Country-wise median imputation
    df = df.sort_values(["Country", "Year"])
    df[numeric_cols] = df.groupby("Country")[numeric_cols].transform(lambda x: x.fillna(x.median()))

    return df

if __name__ == "__main__":
    cleaned = load_and_clean()
    cleaned.to_csv("../data/CleanedDataset.csv", index=False)
    print("Data cleaning completed.")
