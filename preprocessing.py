import os
import pandas as pd
import numpy as np
import math

# vstupy
input_file = "sample_data.csv"
output_file = "preprocessed_data.csv"
df = pd.read_csv(input_file)

if os.path.exists(output_file):
    os.remove(output_file)

def calculate_angle(diff_x, diff_y):
    angle_radians = math.atan2(diff_x, diff_y)
    angle_degrees = math.degrees(angle_radians)

    if angle_degrees < 0:
        angle_degrees += 360

    return angle_degrees

def calculate_tms(x1, y1, x2, y2, time1, time2):
    distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    time_diff = (time2 - time1)
    if time_diff > 0:
        return distance / time_diff
    else:
        return np.nan


processed_data = []
current_touch = None

for _, row in df.iterrows():
    if row['touch_event_type'] == 'down':
        current_touch = {
            "userid": row["userid"],
            "timestamp": row["timestamp"],
            "touch_event_type": row["touch_event_type"],
            "touch_x": row["touch_x"],
            "touch_y": row["touch_y"],
            "direction": np.nan,
            "angle": np.nan
        }
    elif row['touch_event_type'] in ['move', 'up'] and current_touch:
        # Zistíme, či sa pozícia zmenila
        diff_x = row["touch_x"] - current_touch["touch_x"]
        diff_y = row["touch_y"] - current_touch["touch_y"]

        if diff_x == 0 and diff_y == 0 and row['touch_event_type'] == 'move':
            continue
        elif diff_x == 0 and diff_y == 0:
            direction = np.nan
            angle = np.nan
            TMS = np.nan
        else:
            angle = calculate_angle(diff_x, diff_y)
            TMS = calculate_tms(current_touch["touch_x"], current_touch["touch_y"], row["touch_x"], row["touch_y"],
                                current_touch["timestamp"], row["timestamp"])

            match angle:
                case angle if 0 <= angle < 45:
                    direction = 1
                case angle if 45 <= angle < 90:
                    direction = 2
                case angle if 90 <= angle < 135:
                    direction = 3
                case angle if 135 <= angle < 180:
                    direction = 4
                case angle if 180 <= angle < 225:
                    direction = 5
                case angle if 225 <= angle < 270:
                    direction = 6
                case angle if 270 <= angle < 315:
                    direction = 7
                case _:
                    direction = 8

        current_touch = {
            "userid": row["userid"],
            "timestamp": row["timestamp"],
            "touch_event_type": row["touch_event_type"],
            "touch_x": row["touch_x"],
            "touch_y": row["touch_y"],
            "direction": direction,
            "angle": angle,
            "TMS": TMS
        }

    processed_data.append(current_touch)

processed_df = pd.DataFrame(processed_data)
#processed_df.to_csv("temp.csv", index=False)

def create_features(df):
    data = []

    # pre kazdy pohyb daneho usera (pohyb od down po move)
    for _, group in df.groupby('userid'):
        movement_data = None
        direction_data = {i: [] for i in range(1, 9)}

        for _, row in group.iterrows():
            if row["touch_event_type"] == "down":
                if movement_data is not None:
                    for direction in range(1, 9):
                        if direction_data[direction]:
                            movement_data[f"TMS_{direction}"] = np.mean(direction_data[direction])
                        else:
                            movement_data[f"TMS_{direction}"] = np.nan
                    data.append(movement_data)

                movement_data = {
                    "userid": row["userid"],
                }
                direction_data = {i: [] for i in range(1, 9)}

            elif row["touch_event_type"] == "move" and movement_data:
                direction_data[row["direction"]].append(row["TMS"])

            elif row["touch_event_type"] == "up" and movement_data:
                for direction in range(1, 9):
                    if direction_data[direction]:
                        movement_data[f"TMS_{direction}"] = np.mean(direction_data[direction])
                    else:
                        movement_data[f"TMS_{direction}"] = np.nan

                data.append(movement_data)
                movement_data = None

    result_df = pd.DataFrame(data)
    result_df = result_df[["userid"] + [f"TMS_{i}" for i in range(1, 9)]]

    #TODO tu sa bude pokracovat dalse features

    return result_df


final_df = create_features(processed_df)
final_df.to_csv("preprocessed_data.csv", index=False)