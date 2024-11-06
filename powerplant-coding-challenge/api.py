from flask import Flask, jsonify, Response
from powerplant_optimizer import load_payload, prepare_dataframe, optimize_power_output
import pandas as pd

app = Flask(__name__)

@app.route("/productionplan", methods=["GET"])
def production_plan():
    try:
        file_path = "example_payloads/payload3.json"
        payload = load_payload(file_path)
        df = prepare_dataframe(payload)
        load = payload["load"]
        optimized_df = optimize_power_output(df, load)
        response = pd.DataFrame.to_json(optimized_df, orient="records", indent=4)
        return Response(response, mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=8888, debug=True)
