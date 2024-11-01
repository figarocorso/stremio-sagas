from catalog import CATALOG


POSTER_METAHUB_URL = "https://images.metahub.space/poster/medium/{}/img"

def catalog_response(media_type, media_id):
    print(f"Catalog - type: {media_type} - id: {media_id}")
    catalog = CATALOG[media_type] if media_type in CATALOG else []
    metaPreviews = {
        "metas": [
            {
                "id": item["id"],
                "type": media_type,
                "name": item["name"],
                "genres": item["genres"],
                "poster": POSTER_METAHUB_URL.format(item["id"])
            } for item in catalog
        ]
    }
    return metaPreviews
