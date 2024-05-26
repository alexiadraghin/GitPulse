from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_word():
    return "<p>Hello, World!</p>"

@app.route("/api", methods= ["GET"])
def api():
    return jsonify({"message": "Welcome to the API!"})

if __name__ == "__main__":
    app.run(debug=True)