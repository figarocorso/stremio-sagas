from sagas import SAGAS

POSTER_METAHUB_URL = "https://images.metahub.space/poster/medium/{}/img"


def catalog_response(media_type, saga_name):
    return {
        "metas": [
            {
                "id": item["id"],
                "type": media_type,
                "name": item["name"],
                "poster": POSTER_METAHUB_URL.format(item["id"]),
            } for item in SAGAS.get(saga_name, [])
        ]
    }


def get_available_saga_names():
    return list(SAGAS.keys())
