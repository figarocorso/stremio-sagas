MANIFEST = {
    "id": "org.stremio.marathons",
    "version": "1.0.0",
    "name": "Sagas and Marathons",
    "description": "Pack movies into sagas and marathons",
    "logo": "https://www.figarocorso.info/static/images/stremio_sagas.jpg",

    "types": ["movie"],
    "resources": ["catalog"],

    "catalogs": [
        {
            "type": "movie",
            "name": "Marathons & Sagas",
            "id": "sagas",
            "extra": [
                {
                    "name": "Saga Name",
                    "isRequired": True,
                    "options": [
                        "THIS WILL BE DYNAMICALLY UPDATED",
                    ],
                },
            ],
            "extraSupported": ["Saga Name"],
            "extraRequired": ["Saga Name"],
        },
    ],
}
