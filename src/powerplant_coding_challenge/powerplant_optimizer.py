import numpy as np
import pandas as pd


def prepare_dataframe(df, gas, kerosine, wind):
    """
    Prepares a DataFrame from the payload data.
    Args:
        df (pd.DataFrame): The representation of the powerplants from the payload.
        gas (float): The price of gas in euro/MWh.
        kerosine (float): The price of kerosine in euro/MWh.
        wind (float): The percentage of wind.
    Returns:
        pd.DataFrame: The prepared DataFrame with calculated power output, price, and cost.
    """
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
    """
    Sorts the DataFrame by costs and power. It also puts wind turbines on the bottom when there is no wind.
    Args:
        df (pd.DataFrame): The prepared DataFrame.
        wind (float): The percentage of wind.
    Returns:
        pd.DataFrame: The sorted DataFrame.
    """
    filter = (df["type"] == "windturbine") & (wind == 0)
    df["turn_off"] = np.where(filter, 1, 0)
    return df.sort_values(
        by=["turn_off", "cost", "power", "name"], ascending=[True, True, False, True]
    )[["name", "type", "pmin", "power", "cost"]]


def optimize_power_output_without_min(df, load, wind):
    """
    Optimizes the power output without considering minimum load constraints.
    Args:
        df (pd.DataFrame): The sorted DataFrame containing powerplant data.
        load (float): The required load to be met.
        wind (float): The wind percentage.
    Returns:
        pd.DataFrame: The DataFrame with optimized power output.
    """
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


def adjust_to_pmin(df):
    """
    Corrects the optimized output if necessary.
    Args:
        df (pd.DataFrame): The DataFrame with optimized power output, ignoring pmin.
    Returns:
        pd.DataFrame: The DataFrame with corrected power output.
    """
    df["excess"] = np.where(
        df["p_without_min"] == 0,
        0,
        df[["pmin", "p_without_min"]].max(axis=1) - df["p_without_min"],
    )
    df["recover"] = df["excess"].shift(-1, fill_value=0)
    df["p"] = df["p_without_min"] + df["excess"] - df["recover"]
    pd.set_option("display.max_columns", None)
    return df[["name", "p"]]
