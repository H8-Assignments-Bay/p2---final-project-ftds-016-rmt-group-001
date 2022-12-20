from flask import Flask, request, Response
from util.predictutil import predict_or_get_sentiment
from util.stockutil import get_stock_name
import json

app = Flask(__name__)

@app.route('/sentiment')
def get_sentiment():
    args = request.args
    
    symbol = args.get("symbol")
    if symbol == None:
        return "", 400
    
    start_from = args.get("start_from")
    try:
        start_from = int(start_from)
    except (TypeError, ValueError):
        return "", 400
    
    end_at = args.get("end_at")
    try:
        end_at = int(end_at)
    except (TypeError, ValueError):
        return "", 400
    
    sentiment = predict_or_get_sentiment(
        symbol=symbol, start_from=start_from, 
        end_at=end_at)
    
    return Response(
        json.dumps({
            "symbol": symbol,
            "neutral": sentiment['neutral'],
            "negative": sentiment['negative'],
            "positive": sentiment['positive'],
            "comments": sentiment['comments']
        }),
        mimetype='application/json')
    
@app.route('/search')
def query():
    args = request.args
    
    query = args.get("query")
    
    if query == None:
        return "", 400
    
    return get_stock_name(query=query)