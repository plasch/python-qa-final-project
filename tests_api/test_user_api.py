import allure
import requests


@allure.feature("API Tests")
class TestUserAPI:
    api_url = "http://opencart3-oauth.api.opencart-api.com/api/rest_admin"

    def test_login_with_invalid_creds(self, get_access_token):
        url = self.api_url + "/login"
        headers = {"Authorization": f"Bearer {get_access_token}"}
        json_data = {
            "username": "none",
            "password": "none",
        }
        response = requests.request("POST", url, headers=headers, json=json_data)
        assert response.json()["success"] == 0
        assert response.json()["error"] == ["Invalid username or password"]

    def test_login_with_existed_user(self, get_access_token):
        url = self.api_url + "/login"
        headers = {"Authorization": f"Bearer {get_access_token}"}
        json_data = {
            "username": "admin",
            "password": "admin",
        }
        response = requests.request("POST", url, headers=headers, json=json_data)
        assert response.status_code == 200
        assert response.json()["success"] == 1
        assert response.json()["data"]

    def test_get_user_info(self, get_access_token):
        url = self.api_url + "/user"
        headers = {"Authorization": f"Bearer {get_access_token}"}
        response = requests.request("GET", url, headers=headers)
        assert response.status_code == 200
        assert "user_id" in response.json()["data"]

    def test_logout_user(self, get_access_token):
        url = self.api_url + "/logout"
        headers = {"Authorization": f"Bearer {get_access_token}"}
        response = requests.request("POST", url, headers=headers)
        assert response.json()["success"] == 1
        assert response.status_code == 200
