from fastapi import APIRouter, Query
import requests
from ..configs import Configs
import urllib
from typing import Union

router = APIRouter()

@router.get("/event", tags=["event"])
async def event(startDate: Union[str, None] = Query(pattern="^[0-9]{8}$")):   
    
    if startDate is None:
        # emit error
        return None
     
    params = {
        "serviceKey": Configs.TOUR_API_KEY,
        "numOfRows": 15,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "listYN": "Y",
        "arrange": "C",
        "eventStartDate": startDate
    }
    
    safe_params = urllib.parse.urlencode(params, safe='%')
    response = requests.get(Configs.TOUR_API_URL + "/searchFestival1", params = safe_params)
    return response.json()