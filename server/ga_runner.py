import os

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from server.auth.secret import Secret

REFRESH_ERROR = "INVALID REFRESH TOKEN"
_VERSION = "v10"

def create_client(token):
    try:
        secret = Secret(token)
        refresh_token = secret.get_secret_version()
        credentials = {

            "developer_toker": os.environ["DEVELOPER_TOKEN"],
            "client_id": os.environ["CLIENT_ID"],
            "client_secret": os.environ["CLIENT_SECRET"],
            "refresh_token": refresh_token,
            "use_proto_plus":"true"
}
        return GoogleAdsClient.load_from_dict(credentials, version=_VERSION)
    except:
        raise ValueError(REFRESH_ERROR)

def handleGoogleAdsException(ex: GoogleAdsException):

        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")