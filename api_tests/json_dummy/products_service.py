from api_tests.globals import ApiHttpConstants
import requests
from typing import Any, Dict, Optional, Tuple

class products_requests():
    def get_all_products(self,api):
        response = api.get("products")
        return response

    def get_product_by_number(self,api,product_number):
        response = api.get("posts/"+product_number)
        return response
    def create_post(self,api,payload):
        response = api.post("posts", data=payload)
        return response

    def update_post(self,api,payload):
        response = api.put("posts/1", data=payload)
        return response

    def delete_post(self,api,post_number):
        response = api.delete("posts/"+post_number)
        return response

DUMMYJSON_BASE = "https://dummyjson.com"

def login_and_get_tokens(
    username: str,
    password: str,
    expires_in_mins: Optional[int] = 60,
    base_url: str = DUMMYJSON_BASE,
) -> Tuple[Dict[str, Any], requests.Session]:
    """
    Logs in to DummyJSON and returns (response_json, session) where:
      - response_json: parsed JSON including accessToken/refreshToken, etc.
      - session: a requests.Session with cookies set (credentials included)
    """
    session = requests.Session()

    url = f"{base_url}/auth/login"
    payload = {
        "username": username,
        "password": password,
    }
    if expires_in_mins is not None:
        payload["expiresInMins"] = expires_in_mins

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    resp = session.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    # Cookies (e.g., accessToken) are now stored in session.cookies
    # You can use `session` for subsequent authenticated calls.
    return data, session

# Example:
tokens, sess = login_and_get_tokens("emilys", "emilyspass", 30)
print(tokens)
r = sess.get(f"{DUMMYJSON_BASE}/auth/me")
print(r.json())
