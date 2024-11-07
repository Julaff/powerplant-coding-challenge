import pytest

from powerplant_coding_challenge.powerplant_optimizer import (
    prepare_dataframe,
)
from powerplant_coding_challenge.utils import get_fuels, get_powerplants


@pytest.fixture
def payload():
    return {
        "fuels": {"gas(euro/MWh)": 13.4, "kerosine(euro/MWh)": 50.8, "wind(%)": 60},
        "load": 480,
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "tj1",
                "type": "turbojet",
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 16,
            },
            {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150,
            },
        ],
    }


def test_prepare_dataframe(payload):
    gas, kerosine, wind = get_fuels(payload)
    powerplants = get_powerplants(payload)
    df = prepare_dataframe(powerplants, gas, kerosine, wind)
    assert len(df) == 3
    assert "cost" in df.columns
    assert "power" in df.columns
