import pytest
from utils import get_fuels, get_load, get_powerplants

@pytest.fixture
def payload():
    return {
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

def test_get_fuels(payload):
    gas, kerosine, wind = get_fuels(payload)
    assert gas == 13.4
    assert kerosine == 50.8
    assert wind == 60

def test_get_load(payload):
    load = get_load(payload)
    assert load == 480

def test_get_powerplants(payload):
    powerplants = get_powerplants(payload)
    assert len(powerplants) == 3
    assert powerplants[0]["name"] == "gasfiredbig1"
