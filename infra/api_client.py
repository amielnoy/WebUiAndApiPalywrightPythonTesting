import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClient:
    def __init__(self, base_url: str, retries: int = 3, backoff: float = 0.2):
        self.base_url = base_url.rstrip("/")
        self.session = Session()

        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],  # or Retry.DEFAULT_METHOD_WHITELIST
            raise_on_status=False
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _url(self, endpoint: str):
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint, **kwargs):
        return self.session.get(self._url(endpoint), timeout=10, **kwargs)

    def post(self, endpoint, data=None, **kwargs):
        return self.session.post(self._url(endpoint), json=data, timeout=10, **kwargs)

    def put(self, endpoint, data=None, **kwargs):
        return self.session.put(self._url(endpoint), json=data, timeout=10, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.session.delete(self._url(endpoint), timeout=10, **kwargs)
