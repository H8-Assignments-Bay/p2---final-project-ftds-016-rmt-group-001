from flask import Flask, request, Response
from scrapeutil import get_db

app = Flask(__name__)

@app.route('/sentiment')
def get_sentiment():
    args = request.json
    
    symbol = args.get("symbol")
    if symbol == None:
        return "", 400
    
    return Response(get_db(symbol=symbol).to_json(orient="records"), mimetype='application/json')