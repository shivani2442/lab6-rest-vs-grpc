#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import io
import argparse
import base64

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request

    # Convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return Response(
            response=jsonpickle.encode(
                {'error': 'Expected a JSON object containing a and b'}
            ),
            status=400,
            mimetype="application/json"
        )

    a = data.get('a')
    b = data.get('b')

    if not isinstance(a, list) or not isinstance(b, list):
        return Response(
            response=jsonpickle.encode(
                {'error': 'a and b must be lists'}
            ),
            status=400,
            mimetype="application/json"
        )

    if len(a) != len(b):
        return Response(
            response=jsonpickle.encode(
                {'error': 'Vectors must have the same length'}
            ),
            status=400,
            mimetype="application/json"
        )

    if not all(
        isinstance(x, (int, float)) and not isinstance(x, bool)
        for x in a + b
    ):
        return Response(
            response=jsonpickle.encode(
                {'error': 'Vector elements must be numbers'}
            ),
            status=400,
            mimetype="application/json"
        )

    result = sum(x * y for x, y in zip(a, b))

    return Response(
        response=jsonpickle.encode({'dotproduct': result}),
        status=200,
        mimetype="application/json"
    )


@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not isinstance(data.get('image'), str):
        return Response(
            response=jsonpickle.encode(
                {'error': 'Expected a JSON object containing a base64 image'}
            ),
            status=400,
            mimetype="application/json"
        )

    try:
        image_bytes = base64.b64decode(data['image'], validate=True)
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()

        img = Image.open(io.BytesIO(image_bytes))
        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except Exception:
        return Response(
            response=jsonpickle.encode(
                {'error': 'Invalid base64-encoded image'}
            ),
            status=400,
            mimetype="application/json"
        )

    return Response(
        response=jsonpickle.encode(response),
        status=200,
        mimetype="application/json"
    )


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Flask REST server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)
