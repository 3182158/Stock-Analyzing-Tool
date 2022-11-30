import yfinance as yf
from flask import Flask, request, make_response, jsonify

app = Flask("Stock API Service")


# end point to connect with GUI application to send data.
@app.route('/stock', methods=['GET'])
def get_stock():
    try:
        name = request.args.get('name')
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        data = yf.download(name, start_date, end_date)
        return data.to_json(orient='records')
    except:
        return make_response(jsonify('Data not Found! Check Stock ID and Dates'))


if __name__ == '__main__':
    app.run()
