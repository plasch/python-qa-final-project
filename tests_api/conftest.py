import pytest
import requests


@pytest.fixture(scope="session")
def get_access_token():
    url = "http://opencart3-oauth.api.opencart-api.com/api/rest_admin/oauth2/token/client_credentials"
    headers = {"Authorization": "Basic ZGVtb19vYXV0aF9jbGllbnQ6ZGVtb19vYXV0aF9zZWNyZXQ="}
    data = {"grant_type": "client_credentials"}
    response = requests.request("POST", url, headers=headers, data=data)
    assert response.json()["success"] == 1
    access_token = response.json()["data"]["access_token"]
    return access_token
