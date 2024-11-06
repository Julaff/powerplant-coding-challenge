import pandas as pd


def get_fuels(payload):
    return (
        payload["fuels"]["gas(euro/MWh)"],
        payload["fuels"]["kerosine(euro/MWh)"],
        payload["fuels"]["wind(%)"],
    )


def get_load(payload):
    return payload["load"]


def get_powerplants(payload):
    return pd.DataFrame(payload["powerplants"])
