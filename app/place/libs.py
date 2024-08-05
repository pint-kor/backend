from google.oauth2 import service_account
from googleapiclient.discovery import build

CLIENT_SECRET_FILE = './secret/pint-429210-5596b20dcea6.json'
API_SERVICE_NAME = 'places'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)


from enum import Enum

class IncludedType(Enum):
    ART_GALLERY = "art_gallery"
    MUSEUM = "museum"
    BAR = "bar"
    CAFE = "cafe"
    RESTAURANT = "restaurant"
    PARK = "park"