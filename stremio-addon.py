#!/usr/bin/env python3

from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps

from manifest import MANIFEST
from catalog_response import catalog_response

app = Flask(__name__)

def respond_with(data):
    resp = jsonify(data)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    return resp


@app.route("/manifest.json")
def addon_manifest():
    return respond_with(MANIFEST)


@app.route("/catalog/<media_type>/marathon/<saga_param>.json")
def addon_catalog(media_type, saga_param):
    if media_type not in MANIFEST["types"]:
        abort(404)
    saga_name = saga_param.split("=")[-1]
    return respond_with(catalog_response(media_type, saga_name))


if __name__ == "__main__":
    app.run(debug=True)
