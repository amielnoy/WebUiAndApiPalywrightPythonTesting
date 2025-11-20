import requests

class APIClient:
    BASE_URL_API = None
    def __init__(self,base_url: str):
        self.BASE_URL_API = base_url

    def get(self, endpoint, params=None):
        return requests.get(f"{self.BASE_URL_API}/{endpoint}", params=params)

    def post(self, endpoint, data=None):
        return requests.post(f"{self.BASE_URL_API}/{endpoint}", json=data)

    def put(self, endpoint, data=None):
        return requests.put(f"{self.BASE_URL_API}/{endpoint}", json=data)

    def delete(self, endpoint):
        return requests.delete(f"{self.BASE_URL_API}/{endpoint}")
