from flask import Flask, jsonify
import json

file = open("example_payloads/response3.json")
response = json.load(file)

app = Flask(__name__)


@app.route("/productionplan", methods=["GET"])
def hello_world():
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8888, debug=True)
