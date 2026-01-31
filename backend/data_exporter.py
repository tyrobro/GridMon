import sqlite3
import pandas as pd


def exporter():
    conn = sqlite3.connect("gridmon.db")
    df = pd.read_sql_query("SELECT * FROM logs", conn)

    conn.close()

    print(f"Total records harvested: {len(df)}")

    if len(df) < 50:
        print("Not enough data.")
    else:
        df.to_csv("training_data.csv", index=False)
        print("Data has been exported.")
        print(df.head())


if __name__ == "__main__":
    exporter()
