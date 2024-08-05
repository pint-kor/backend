from fastapi import APIRouter, Query
from .libs import credentials, IncludedType
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from typing import Optional, Union

router = APIRouter()

def requestBuilder(http, *args, **kwargs):
    headers = kwargs.get('headers', {})
    headers['X-Goog-FieldMask'] = 'places.displayName,places.formattedAddress,places.id,places.photos,places.location'
    kwargs['headers'] = headers
    return HttpRequest(http, *args, **kwargs)

@router.get("/places:nearbyQuery")
def get_place_nearBy(
    latitude: float = Query(None),
    longitude: float = Query(None),
    radius: int = Query(None),
    languageCode: str = Query("ko"),
    maxResultCount: int = Query(20)
):
    with build("places", "v1", credentials=credentials, requestBuilder=requestBuilder) as service:
        response = service.places().searchNearby(
            body={
                "locationRestriction": {
                    "circle": {
                        "center": {
                            "latitude": latitude,
                            "longitude": longitude
                        },
                        "radius": radius
                    }
                },
                "languageCode": languageCode,
                "maxResultCount": maxResultCount
            }
        ).execute()

        return response
    

@router.get("/places:textQuery")
def get_place(
    query: str = Query(None),
    latitude: Union[float, None] = Query(None),
    longitude: Union[float, None] = Query(None),
    radius: Union[int, None] = Query(None),
    languageCode: str = Query('ko'),
    includedType: Union[IncludedType, None] = Query(None)
):
    def requestBuilder(http, *args, **kwargs):
        headers = kwargs.get('headers', {})
        headers['X-Goog-FieldMask'] = 'places.displayName,places.formattedAddress,places.id,places.photos,places.location,places.primaryType'
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
                "languageCode": languageCode,
                "includedType": includedType.value if includedType else None
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