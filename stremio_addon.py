#!/usr/bin/env python3

from flask import Flask, jsonify, abort

from manifest import MANIFEST
from catalog_response import catalog_response, get_available_saga_names

app = Flask(__name__)


def respond_with(data):
    response = jsonify(data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


@app.route("/manifest.json")
def addon_manifest():
    manifest = set_manifest_sagas_from_available_sagas(MANIFEST)
    return respond_with(manifest)


@app.route("/catalog/<media_type>/sagas/<saga_param>.json")
def addon_catalog(media_type, saga_param):
    if media_type not in MANIFEST["types"]:
        abort(404)
    saga_name = saga_param.split("=")[-1]
    return respond_with(catalog_response(media_type, saga_name))


def set_manifest_sagas_from_available_sagas(manifest):
    manifest["catalogs"][0]["extra"][0]["options"] = get_available_saga_names()
    return manifest


if __name__ == "__main__":
    app.run(debug=True)
