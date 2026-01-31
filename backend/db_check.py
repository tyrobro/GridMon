import sqlite3


def check_data():
    try:
        conn = sqlite3.connect("gridmon.db")
        cursor = conn.cursor()

        print("--- Checking GridMon Vault ---")
        cursor.execute("SELECT * FROM logs")

        rows = cursor.fetchall()

        if not rows:
            print("Result: The database is EMPTY.")
            print("Diagnosis: The 'INSERT' command in your server.py is not working.")
        else:
            print(f"Result: Success! Found {len(rows)} records.")
            print("Here are the last 3 entries:")
            for row in rows[-3:]:
                print(row)

        conn.close()

    except sqlite3.OperationalError as e:
        print("ERROR: Could not read database.")
        print(f"Details: {e}")
        print("Diagnosis: The table 'logs' probably hasn't been created yet.")


if __name__ == "__main__":
    check_data()
