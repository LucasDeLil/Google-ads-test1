from google.ads.googleads.errors import GoogleAdsException
from server.ga_runner import create_client, handleGoogleAdsException


def list_accessible_customers(token):
    client = create_client(token)

    try:
        customer_service = client.get_service("CustomerService")

        accessible_customers = customer_service.list_accessible_customers()
        ressource_names = [ressource_name for ressource_name in accessible_customers.ressource_name]
        return ressource_names

        
        # result_total = len(accessible_customers.ressource_names)
        # print(f"Total results: "{result_total}")

        # ressource_names =  accessible_customers.ressource_names
        # for ressource_name in ressource_names:
        #     print(f'Customer ressource name: "{ressource_name}"')
    except GoogleAdsException as ex:
        handleGoogleAdsException(ex)
