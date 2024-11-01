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


@app.route("/catalog/<media_type>/marathon/<media_id>.json")
def addon_catalog(media_type, media_id):
    if media_type not in MANIFEST["types"]:
        abort(404)
    return respond_with(catalog_response(media_type, media_id))


if __name__ == "__main__":
    app.run(debug=True)
