import pandas as pd


def get_fuels(payload):
    """
    Extracts fuel information from the payload.
    Args:
        payload (dict): The input data containing fuels.
    Returns:
        tuple: A tuple containing gas, kerosine, and wind values.
    """
    try:
        return (
            payload["fuels"]["gas(euro/MWh)"],
            payload["fuels"]["kerosine(euro/MWh)"],
            payload["fuels"]["wind(%)"],
        )
    except KeyError as e:
        raise ValueError(f"Missing key in payload: {e}")


def get_load(payload):
    """
    Extracts the load value from the payload.
    Args:
        payload (dict): The input data containing the load.
    Returns:
        float: The load value.
    """
    try:
        return payload["load"]
    except KeyError as e:
        raise ValueError(f"Missing key in payload: {e}")


def get_powerplants(payload):
    """
    Extracts powerplant information from the payload.
    Args:
        payload (dict): The input data containing powerplants.
    Returns:
        pd.DataFrame: A DataFrame of powerplants.
    """
    try:
        return pd.DataFrame(payload["powerplants"])
    except KeyError as e:
        raise ValueError(f"Missing key in payload: {e}")
