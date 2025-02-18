from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/debug", methods=["GET"])
def test_get():
	return jsonify({"message": "test"})

@app.route("/api/debug", methods=["POST"])
def test_post():
	data = request.json
	print(data)
	try:
		startDate = data.get("startDate")
		endDate = data.get("endDate")

	except Exception as e:
		print("error")
		print(e)

	res = jsonify({"message": "hello"})
	return res


if __name__ == "__main__":
	app.run(debug=True, port=8080)