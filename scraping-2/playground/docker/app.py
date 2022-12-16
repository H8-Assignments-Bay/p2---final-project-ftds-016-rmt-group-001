from flask import Flask

app = Flask(__name__)

@app.route("/sentiment")
def sentiment():
    return "Hello World", 200