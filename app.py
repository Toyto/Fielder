from flask import Flask, request, jsonify
from utils import StatExtractor, ValuesExtractor


app = Flask(__name__)


@app.route('/equidistant-point')
def get_equidistant_point():
    coords = request.args.get('coordinates').replace(' ', ',')
    distance = request.args.get('distance')
    extractor = ValuesExtractor()
    result = extractor.equidistant_point(coords, distance)
    return jsonify(result)


@app.route('/rectangle')
def get_rectangle():
    coords = request.args.get('coordinates').replace(' ', ',')
    extractor = ValuesExtractor()
    result = extractor.rectangle(coords)
    return jsonify(result)


@app.route('/region-stat')
def region_stat():
    region = request.args.get('region')
    extractor = StatExtractor()
    result = extractor.get_region(region)
    return jsonify(result)
