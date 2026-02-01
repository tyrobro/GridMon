import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib


def train_brain():
    print("Loading Data")
    try:
        df = pd.read_csv("training_data.csv")
        features = ["cpu_usage", "memory_usage"]
        X = df[features]

        print("Data Info:")
        print(df[features].describe())
        print("-" * 30)

        print(f"Training on {len(df)} records.")
        model = IsolationForest(contamination=0.01, random_state=7)
        model.fit(X)

        joblib.dump(model, "model.pkl")
        print("Model trained and saved to model.pkl")

        test_normal = pd.DataFrame([(5.0, 40.0)], columns=features)
        test_crazy = pd.DataFrame([(99.9, 90.0)], columns=features)

        print(f"Test Normal {test_normal}: {model.predict(test_normal)}")
        print(f"Test crazy {test_crazy}: {model.predict(test_crazy)}")

    except FileNotFoundError:
        print("training_data.csv not found. Run the exporter first.")


if __name__ == "__main__":
    train_brain()
