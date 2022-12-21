from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route("/sentiment")
def sentiment():
    args = request.args
    
    symbol = args.get("symbol")
    start_from = args.get("start_from")
    end_at = args.get("end_at")
    
    return Response(
        response=json.dumps(
            {
                "symbol": symbol,
                "start_from": start_from,
                "end_at": end_at
            }
        ), mimetype='application/json'
    ), 200