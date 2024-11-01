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
