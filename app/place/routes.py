from fastapi import APIRouter, Query
from .libs import credentials, IncludedType
from .models import Place
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from typing import Optional, Union, List
from bson import ObjectId

router = APIRouter()

def requestBuilder(http, *args, **kwargs):
    headers = kwargs.get('headers', {})
    headers['X-Goog-FieldMask'] = 'places.displayName,places.formattedAddress,places.id,places.photos,places.location'
    kwargs['headers'] = headers
    return HttpRequest(http, *args, **kwargs)

@router.get("/api/google/places:nearbyQuery")
def get_place_nearBy_at_google(
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
    

@router.get("/api/google/places:textQuery")
def get_place_at_google(
    query: str = Query(None),
    latitude: Union[float, None] = Query(None),
    longitude: Union[float, None] = Query(None),
    radius: Union[int, None] = Query(None),
    languageCode: str = Query('ko'),
    includedType: Union[IncludedType, None] = Query(None),
    pageSize: int = Query(20),
    pageToken: str = Query(None)
):
    if not query:
        return None
    
    def requestBuilder(http, *args, **kwargs):
        headers = kwargs.get('headers', {})
        headers['X-Goog-FieldMask'] = 'places.displayName,places.formattedAddress,places.id,places.photos,places.location,places.primaryType,nextPageToken'
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
                "pageSize": pageSize,
                "languageCode": languageCode,
                "includedType": includedType.value if includedType else None,
                "pageToken": pageToken
            }
        ).execute()
        return response
    
@router.get("/api/google/places/{placeId}")
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
    
@router.post("/api/pint/places")
async def register_new_place(
    place: Place
):
    # check if the place already exists
    place_exist = await Place.find_one(Place.googlePlaceId == place.googlePlaceId)
    if place_exist:
        return place

    await place.save()
    return place

@router.get("/api/pint/places", response_model=List[Place])
async def get_place(
    placeName: str = Query(None),
    googlePlaceId: str = Query(None),
):
    query = {}
    
    if googlePlaceId:
        query["googlePlaceId"] = googlePlaceId
    
    if placeName:
        # query["$text"] = {"$search": placeName}
        query["placeName"] = {"$regex": placeName, "$options": "i"}
    
    places = await Place.find(query).to_list()
    return places

@router.get("/api/pint/places/{id}")
async def get_place_by_id(
    id: str
) -> Place | None:
    if (not ObjectId.is_valid(id)):
        return None
    
    place = await Place.get(id)
    return place