import logging

from flask import Flask, Response, jsonify, request
from powerplant_optimizer import (
    adjust_to_pmin,
    optimize_power_output_without_min,
    prepare_dataframe,
)
from utils import get_fuels, get_load, get_powerplants

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/productionplan", methods=["POST"])
def production_plan():
    """
    Endpoint to handle production plan requests.
    """
    try:
        payload = request.get_json()

        gas, kerosine, wind = get_fuels(payload)
        load = get_load(payload)
        df = get_powerplants(payload)
        prepared_df = prepare_dataframe(df, gas, kerosine, wind)
        optimized_df_without_min = optimize_power_output_without_min(
            prepared_df, load, wind
        )
        optimized_df = adjust_to_pmin(optimized_df_without_min)
        response = optimized_df.to_json(orient="records", indent=4)
        return Response(response, mimetype="application/json")
    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
    except KeyError as ke:
        logging.error(f"KeyError: {ke}")
        return jsonify({"error": f"Missing key: {ke}"}), 400
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    app.run(port=8888, debug=True, host='0.0.0.0')
