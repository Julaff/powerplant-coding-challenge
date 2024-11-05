import json
import numpy as np
import pandas as pd


def main():
    file = open("example_payloads/payload3.json")
    payload = json.load(file)

    load = payload["load"]

    for plant in payload["powerplants"]:
        plantType = plant["type"]
        if plantType == "windturbine":
            print("Wind turbine found")
            price = 0
            print(f"price is {price}")
            p = plant["pmax"] * payload["fuels"]["wind(%)"] / 100
            print(f"p = {p}")
        elif plantType == "gasfired":
            print("Gas fired plant found")
            price = payload["fuels"]["gas(euro/MWh)"]
            print(f"price is {price}")
            p = plant["pmax"]
            print(f"p = {p}")
        elif plantType == "turbojet":
            print("Turbojet found")
            price = payload["fuels"]["kerosine(euro/MWh)"]
            print(f"price is {price}")
            p = plant["pmax"]
            print(f"p = {p}")
        else:
            print("Unknown plant type found")
        cost = price / plant["efficiency"]
        print(f"Cost is {cost}")
        print("---")

    print(load)

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

    dfSorted = df.sort_values(by=["cost", "p"], ascending=[True, False])

    dfSorted["remainingLoadAfter"] = np.maximum(load - dfSorted["p"].cumsum(), 0)
    dfSorted["remainingLoadBefore"] = dfSorted["remainingLoadAfter"].shift(
        1, fill_value=load
    )
    dfSorted["response"] = (
        dfSorted["remainingLoadBefore"] - dfSorted["remainingLoadAfter"]
    )

    pd.set_option("display.max_columns", None)
    print(dfSorted)

    result = dfSorted[["name", "response"]]

    dict_result = result.to_dict(orient="records")

    print(json.dumps(dict_result, indent=4))


if __name__ == "__main__":
    main()
