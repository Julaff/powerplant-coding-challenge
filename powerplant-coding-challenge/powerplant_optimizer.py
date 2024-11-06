import numpy as np
import pandas as pd


def prepare_dataframe(df, gas, kerosine, wind):
    conditions = [
        df["type"] == "gasfired",
        df["type"] == "turbojet",
        df["type"] == "windturbine",
    ]
    power = [df["pmax"], df["pmax"], df["pmax"] * wind / 100]
    price = [
        gas,
        kerosine,
        0,
    ]
    df["power"] = np.select(conditions, power, default=0)
    df["price"] = np.select(conditions, price, default=0)
    df["cost"] = df["price"] / df["efficiency"]
    return df[["name", "type", "pmin", "power", "cost"]]


def sort_dataframe(df, wind):
    df["ignore"] = np.where((df["type"] == "windturbine") & (wind == 0), 1, 0)
    return df.sort_values(
        by=["ignore", "cost", "power"], ascending=[True, True, False]
    )[["name", "type", "pmin", "power", "cost"]]


def optimize_power_output_without_min(df, load, wind):
    df_sorted = sort_dataframe(df, wind)
    df_sorted["remaining_load_after"] = np.maximum(
        load - df_sorted["power"].cumsum(), 0
    )
    df_sorted["remaining_load_before"] = df_sorted["remaining_load_after"].shift(
        1, fill_value=load
    )
    df_sorted["p_without_min"] = (
        df_sorted["remaining_load_before"] - df_sorted["remaining_load_after"]
    )
    return df_sorted[["name", "pmin", "p_without_min"]]


def correct_excess(df):
    df["excess"] = np.where(
        df["p_without_min"] == 0,
        0,
        df[["pmin", "p_without_min"]].max(axis=1) - df["p_without_min"],
    )
    df["recover"] = df["excess"].shift(-1, fill_value=0)
    df["p"] = df["p_without_min"] + df["excess"] - df["recover"]
    pd.set_option("display.max_columns", None)
    return df[["name", "p"]]
