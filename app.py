from flask import Flask, request, jsonify
from utils import ValuesExtractor


app = Flask(__name__)


@app.route('/equidistant-point')
def get_equidistant_point():
    coords = request.args.get('coordinates').replace(' ', ',')
    distance = request.args.get('distance')
    extractor = ValuesExtractor()
    result = extractor.equidistant_point(coords, distance)
    return jsonify(result)
