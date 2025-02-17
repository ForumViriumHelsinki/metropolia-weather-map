from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
	return "Home"

@app.route("/api/test", methods=["GET"])
def test_get():
	print("test")
	return jsonify({"message": "test get"})

if __name__ == "__main__":
	app.run(debug=True, port=8080)