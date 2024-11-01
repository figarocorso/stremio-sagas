#!/usr/bin/env python3

from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps

from manifest import MANIFEST
from catalog import CATALOG


# This is template we"ll be using to construct URL for the item poster
METAHUB_URL = "https://images.metahub.space/poster/medium/{}/img"

app = Flask(__name__)


def respond_with(data):
    resp = jsonify(data)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    return resp


@app.route("/manifest.json")
def addon_manifest():
    return respond_with(MANIFEST)


@app.route("/catalog/<type>/marathon/<id>.json")
def addon_catalog(type, id):
    print(f"Catalog - type: {type} - id: {id}")
    if type not in MANIFEST["types"]:
        abort(404)

    catalog = CATALOG[type] if type in CATALOG else []
    metaPreviews = {
        "metas": [
            {
                "id": item["id"],
                "type": type,
                "name": item["name"],
                "genres": item["genres"],
                "poster": METAHUB_URL.format(item["id"])
            } for item in catalog
        ]
    }
    return respond_with(metaPreviews)


if __name__ == "__main__":
    app.run(debug=True)
