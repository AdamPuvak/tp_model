import requests
import pandas as pd

# endpoint
BASE_URL = "https://biopassword.jecool.net/db/getTable.php?table="

# gets single table
def get_data(table_name):
    url = f"{BASE_URL}{table_name}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting data from {table_name}: {response.status_code}")
        return None

# gets all tables
def load_all_data():
    tables = ['accelerometer', 'gyroscope', 'orientation', 'touch']
    data = {}

    for table in tables:
        data[table] = get_data(table)

    return data

# preprocesses columns in tables
def preprocess_tables(all_data):
    processed_data = {}

    for table, data in all_data.items():
        if data:
            df = pd.DataFrame(data)

            # deletes column "input"
            if "input" in df.columns:
                df = df.drop(columns=["input"])

            if table in ["accelerometer", "gyroscope"]:
                # deletes column "userid"
                if "userid" in df.columns:
                    df = df.drop(columns=["userid"])

                # renames axes columns
                rename_dict = {col: f"{table}_{col}" for col in ["x", "y", "z"] if col in df.columns}
                df = df.rename(columns=rename_dict)

            if table == "orientation":
                # deletes column "userid"
                if "userid" in df.columns:
                    df = df.drop(columns=["userid"])


            if table == "touch":
                # deletes other columns (temporary)
                df = df.drop(columns=["event_type_detail", "pointer_id", "raw_x", "raw_y", "touch_major", "touch_minor"])

                # renames touch-related columns
                rename_dict = {col: f"{table}_{col}" for col in ["event_type", "x", "y", "pressure", "size"] if col in df.columns}
                df = df.rename(columns=rename_dict)

            processed_data[table] = df

    return processed_data

# merges all tables into one by timestamp
def merge_data(processed_data):
    dfs = {}

    for table, data in processed_data.items():
        if not data.empty:
            df = pd.DataFrame(data)
            dfs[table] = df

    merged_df = None
    for table, df in dfs.items():
        df = df.sort_values("timestamp")

        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on="timestamp", how="outer")

    return merged_df

def fill_missing_touch_data(df):
    touch_columns = ['touch_event_type', 'touch_x', 'touch_y', 'touch_pressure', 'touch_size']
    
    for col in touch_columns:
        if col in df.columns:
            last_valid_value = None
            
            for i in range(len(df)):
                if pd.notna(df.at[i, col]):
                    last_valid_value = df.at[i, col]
                elif last_valid_value is not None:
                    df.at[i, col] = last_valid_value
    return df

# saves merged_df to CSV
def save_to_csv(merged_df, filename="from_database_data.csv"):
    column_order = [
        "userid", "timestamp", "orientation", "touch_event_type", "touch_x", "touch_y", "touch_pressure", "touch_size",
        "accelerometer_x", "accelerometer_y", "accelerometer_z",
        "gyroscope_x", "gyroscope_y", "gyroscope_z"
    ]

    merged_df = merged_df[[col for col in column_order if col in merged_df.columns]]

    merged_df.to_csv(filename, index=False)

# only runs in this file
if __name__ == "__main__":
    all_data = load_all_data()
    processed_data = preprocess_tables(all_data)
    merged_df = merge_data(processed_data)
    save_to_csv(merged_df)

    merged_df = fill_missing_touch_data(merged_df)
    save_to_csv(merged_df, "from_database_data_filled.csv")
