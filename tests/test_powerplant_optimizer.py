import pytest
from powerplant_coding_challenge.powerplant_optimizer import (
    prepare_dataframe,
    optimize_power_output_without_min,
    adjust_to_pmin,
)


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
    df = prepare_dataframe(payload)
    assert len(df) == 3
    assert "cost" in df.columns
    assert "p" in df.columns


def test_optimize_power_output_without_min(payload):
    df = prepare_dataframe(payload)
    load = payload["load"]
    wind = payload["fuels"]["wind(%)"]
    optimized_df = optimize_power_output_without_min(df, load, wind)
    assert len(optimized_df) == 3
    assert "remaining_load_after" in optimized_df.columns
    assert "remaining_load_before" in optimized_df.columns


def test_adjust_to_pmin(payload):
    df = prepare_dataframe(payload)
    load = payload["load"]
    wind = payload["fuels"]["wind(%)"]
    optimized_df = optimize_power_output_without_min(df, load, wind)
    corrected_df = adjust_to_pmin(optimized_df)
    assert len(corrected_df) == 3
    assert "name" in corrected_df.columns
    assert "p" in corrected_df.columns
