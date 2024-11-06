import json
import numpy as np
import pandas as pd


def load_payload(file_path):
    with open(file_path, "r") as file:
        payload = json.load(file)
    return payload


def prepare_dataframe(payload):
    df = pd.DataFrame(payload["powerplants"])
    conditions = [
        df["type"] == "gasfired",
        df["type"] == "turbojet",
        df["type"] == "windturbine",
    ]
    p = [df["pmax"], df["pmax"], df["pmax"] * payload["fuels"]["wind(%)"] / 100]
    price = [
        payload["fuels"]["gas(euro/MWh)"],
        payload["fuels"]["kerosine(euro/MWh)"],
        0,
    ]
    df["p"] = np.select(conditions, p, default=0)
    df["price"] = np.select(conditions, price, default=0)
    df["cost"] = df["price"] / df["efficiency"]
    return df


def optimize_power_output(df, load):
    df_sorted = df.sort_values(by=["cost", "p"], ascending=[True, False])
    df_sorted["remaining_load_after"] = np.maximum(load - df_sorted["p"].cumsum(), 0)
    df_sorted["remaining_load_before"] = df_sorted["remaining_load_after"].shift(
        1, fill_value=load
    )
    df_sorted["p"] = (
        df_sorted["remaining_load_before"] - df_sorted["remaining_load_after"]
    )
    pd.set_option("display.max_columns", None)
    print(df_sorted)
    return df_sorted[["name", "p"]]


def main():
    file_path = "example_payloads/payload3.json"
    payload = load_payload(file_path)
    load = payload["load"]
    df = prepare_dataframe(payload)
    result = optimize_power_output(df, load)
    result_json = pd.DataFrame.to_json(result, orient="records", indent=4)
    print(result_json)
    return result_json


if __name__ == "__main__":
    main()
