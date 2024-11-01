#!/usr/bin/env python3

from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps

MANIFEST = {
    "id": "org.stremio.marathons_python",
    "version": "1.0.0",
    "name": "Sagas and Marathons in Python",
    "description": "Pack movies into sagas and marathons",

    "types": ["movie"],
    "resources": ["catalog"],

    "catalogs": [
        {
            "type": "movie",
            "name": "Marathons Python",
            "id": "marathon",
            "extra": [
                {
                    "name": "Saga Name",
                    "isRequired": True,
                    "options": [
                        "Lord of the Rings",
                        "Harry Potter",
                        "Arnold Chuache",
                    ],
                },
            ],
            "extraSupported": ["Saga Name"],
            "extraRequired": ["Saga Name"],
        },
    ],
}

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

STREAMS = {
    "movie": {
        "tt0032138": [
            {"title": "Torrent",
                "infoHash": "24c8802e2624e17d46cd555f364debd949f2c81e", "fileIdx": 0}
        ],
        "tt0017136": [
            {"title": "Torrent",
                "infoHash": "dca926c0328bb54d209d82dc8a2f391617b47d7a", "fileIdx": 1}
        ],
        "tt0051744": [
            {"title": "Torrent", "infoHash": "9f86563ce2ed86bbfedd5d3e9f4e55aedd660960"}
        ],
        "tt1254207": [
            {"title": "HTTP URL", "url": "http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"}
        ],
        "tt0031051": [
            {"title": "YouTube", "ytId": "m3BKVSpP80s"}
        ],
        "tt0137523": [
            {"title": "External URL",
                "externalUrl": "https://www.netflix.com/watch/26004747"}
        ]
    },

    "series": {
        "tt1748166:1:1": [
            {"title": "Torrent", "infoHash": "07a9de9750158471c3302e4e95edb1107f980fa6"}
        ],

        "hpytt0147753:1:1": [
            {"title": "YouTube", "ytId": "5EQw5NYlbyE"}
        ],
        "hpytt0147753:1:2": [
            {"title": "YouTube", "ytId": "ZzdBKcVzx9Y"}
        ]
    }
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


@app.route("/stream/<type>/<id>.json")
def addon_stream(type, id):
    if type not in MANIFEST["types"]:
        abort(404)

    streams = {"streams": []}
    if type in STREAMS and id in STREAMS[type]:
        streams["streams"] = STREAMS[type][id]
    return respond_with(streams)


if __name__ == "__main__":
    print(MANIFEST)
    app.run(debug=True)
