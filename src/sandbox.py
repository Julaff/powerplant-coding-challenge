import json
import pandas as pd
import numpy as np

file = open("example_payloads/payload3.json")
p3 = json.load(file)

load = p3["load"]

for plant in p3["powerplants"]:
    ptype = plant["type"]
    if ptype == "windturbine":
        print("Wind turbine found")
        price = 0
        print(f"price is {price}")
        p = plant["pmax"] * p3["fuels"]["wind(%)"] / 100
        print(f"p = {p}")
    elif ptype == "gasfired":
        print("Gas fired plant found")
        price = p3["fuels"]["gas(euro/MWh)"]
        print(f"price is {price}")
        p = plant["pmax"]
        print(f"p = {p}")
    elif ptype == "turbojet":
        print("Turbojet found")
        price = p3["fuels"]["kerosine(euro/MWh)"]
        print(f"price is {price}")
        p = plant["pmax"]
        print(f"p = {p}")
    else:
        print("Unknown plant type found")
    cost = price / plant["efficiency"]
    print(f"Cost is {cost}")
    print('---')

print(load)

df = pd.DataFrame(p3["powerplants"])

conditions = [df["type"] == "gasfired", df["type"] == "turbojet", df["type"] == "windturbine"]
p = [df["pmax"], df["pmax"], df["pmax"] * p3["fuels"]["wind(%)"] / 100]
price = [p3["fuels"]["gas(euro/MWh)"], p3["fuels"]["kerosine(euro/MWh)"], 0]

df["p"] = np.select(conditions, p, default=0)
df["price"] = np.select(conditions, price, default=0)
df["cost"] = df["price"] / df["efficiency"]

df2 = df.sort_values(by=['cost', 'p'], ascending=[True, False])

df2["new"] = np.maximum(load - df2["p"].cumsum(), 0)
df2["new2"] = df2["new"].shift(1)
df2["new3"] = df2[["new2", "p"]].min(axis=1)

result = df2[['name', 'new3']]

dict_result = result.to_dict(orient='records')

print(json.dumps(dict_result, indent=4))

