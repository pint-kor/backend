from fastapi import APIRouter, Query
from .libs import credentials
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

router = APIRouter()

@router.get("/places")
def get_place(
    query: str = Query(None),
    latitude: float = Query(None),
    longitude: float = Query(None),
    radius: int = Query(5000),
    languageCode: str = Query('ko')
):
    def requestBuilder(http, *args, **kwargs):
        headers = kwargs.get('headers', {})
        headers['X-Goog-FieldMask'] = 'places.displayName,places.formattedAddress,places.id,places.photos,places.location'
        kwargs['headers'] = headers
        return HttpRequest(http, *args, **kwargs)
    
    with build("places", "v1", credentials=credentials, requestBuilder=requestBuilder) as service:
        response = service.places().searchText(
            body={
                "textQuery": query,
                "locationBias": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": radius,
                    }
                },
                "pageSize": 20,
                "languageCode": languageCode
            }
        ).execute()
        return response
    
@router.get("/places/{placeId}")
def get_place_detail(
    placeId: str
):
    
    def requestBuilder(http, *args, **kwargs):
        headers = kwargs.get('headers', {})
        headers['X-Goog-FieldMask'] = 'places.displayName,places.formattedAddress,places.id,places.photos,places.location'
        kwargs['headers'] = headers
        return HttpRequest(http, *args, **kwargs)
    
    with build("places", "v1", credentials=credentials, requestBuilder=requestBuilder) as service:
        response = service.places().get(
            name=placeId
        ).execute()
        return response