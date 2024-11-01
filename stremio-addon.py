#!/usr/bin/env python3

from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps

from manifest import MANIFEST


CATALOG = {
    "movie": [
        {"id": "tt0032138", "name": "The Wizard of Oz", "genres": [
            "Adventure", "Family", "Fantasy", "Musical"]},
        {"id": "tt0017136", "name": "Metropolis",
         "genres": ["Drama", "Sci-Fi"]},
        {"id": "tt0051744", "name": "House on Haunted Hill",
         "genres": ["Horror", "Mystery"]},
        {"id": "tt1254207", "name": "Big Buck Bunny",
         "genres": ["Animation", "Short", "Comedy"], },
        {"id": "tt0031051", "name": "The Arizona Kid",
         "genres": ["Music", "War", "Western"]},
        {"id": "tt0137523", "name": "Fight Club", "genres": ["Drama"]}
    ],
}


# This is template we"ll be using to construct URL for the item poster
METAHUB_URL = "https://images.metahub.space/poster/medium/{}/img"

OPTIONAL_META = ["posterShape", "background", "logo", "videos", "description", "releaseInfo", "imdbRating", "director", "cast",
                 "dvdRelease", "released", "inTheaters", "certification", "runtime", "language", "country", "awards", "website", "isPeered"]

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


@app.route("/meta/<type>/<id>.json")
def addon_meta(type, id):
    if type not in MANIFEST["types"]:
        abort(404)

    def mk_item(item):
        meta = dict((key, item[key])
                    for key in item.keys() if key in OPTIONAL_META)
        meta["id"] = item["id"]
        meta["type"] = type
        meta["name"] = item["name"]
        meta["genres"] = item["genres"]
        meta["poster"] = METAHUB_URL.format(item["id"])
        return meta

    meta = {
        "meta": next((mk_item(item)
                      for item in CATALOG[type] if item["id"] == id),
                     None)
    }

    return respond_with(meta)


if __name__ == "__main__":
    print(MANIFEST)
    app.run(debug=True)
