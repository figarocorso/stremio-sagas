MANIFEST = {
    "id": "org.stremio.marathons",
    "version": "1.0.0",
    "name": "Sagas and Marathons",
    "description": "Pack movies into sagas and marathons",

    "types": ["movie"],
    "resources": ["catalog"],

    "catalogs": [
        {
            "type": "movie",
            "name": "Marathons & Sagas",
            "id": "marathons",
            "extra": [
                {
                    "name": "Saga Name",
                    "isRequired": True,
                    "options": [
                        "Lord of the Rings",
                        "Harry Potter",
                    ],
                },
            ],
            "extraSupported": ["Saga Name"],
            "extraRequired": ["Saga Name"],
        },
    ],
}
