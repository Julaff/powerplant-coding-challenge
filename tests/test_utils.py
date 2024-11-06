import unittest
from utils import get_fuels, get_load, get_powerplants

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.payload = {
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "wind(%)": 60
            },
            "load": 480,
            "powerplants": [
                {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
                {"name": "tj1", "type": "turbojet", "efficiency": 0.3, "pmin": 0, "pmax": 16},
                {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150}
            ]
        }

    def test_get_fuels(self):
        gas, kerosine, wind = get_fuels(self.payload)
        self.assertEqual(gas, 13.4)
        self.assertEqual(kerosine, 50.8)
        self.assertEqual(wind, 60)

    def test_get_load(self):
        load = get_load(self.payload)
        self.assertEqual(load, 480)

    def test_get_powerplants(self):
        powerplants = get_powerplants(self.payload)
        self.assertEqual(len(powerplants), 3)
        self.assertEqual(powerplants[0]["name"], "gasfiredbig1")

if __name__ == "__main__":
    unittest.main()
