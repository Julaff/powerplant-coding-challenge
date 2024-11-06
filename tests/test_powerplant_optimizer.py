import unittest
import pandas as pd
from powerplant_optimizer import prepare_dataframe, optimize_power_output_without_min, correct_excess

class TestPowerplantOptimizer(unittest.TestCase):

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

    def test_prepare_dataframe(self):
        df = prepare_dataframe(self.payload)
        self.assertEqual(len(df), 3)
        self.assertIn("cost", df.columns)
        self.assertIn("p", df.columns)

    def test_optimize_power_output_without_min(self):
        df = prepare_dataframe(self.payload)
        load = self.payload["load"]
        wind = self.payload["fuels"]["wind(%)"]
        optimized_df = optimize_power_output_without_min(df, load, wind)
        self.assertEqual(len(optimized_df), 3)
        self.assertIn("remaining_load_after", optimized_df.columns)
        self.assertIn("remaining_load_before", optimized_df.columns)

    def test_correct_excess(self):
        df = prepare_dataframe(self.payload)
        load = self.payload["load"]
        wind = self.payload["fuels"]["wind(%)"]
        optimized_df = optimize_power_output_without_min(df, load, wind)
        corrected_df = correct_excess(optimized_df)
        self.assertEqual(len(corrected_df), 3)
        self.assertIn("name", corrected_df.columns)
        self.assertIn("p", corrected_df.columns)

if __name__ == "__main__":
    unittest.main()
