# infra/api_session.py
from typing import Any, Dict, Optional
from infra.base_session import BaseSession
from infra.api_client import APIClient


class APISession(BaseSession):
    def __init__(self, base_url: str, env: str = "local", metadata: Optional[Dict[str, Any]] = None):
        super().__init__(session_type="api", env=env, metadata=metadata)
        self.client = APIClient(base_url)

    def open(self) -> None:
        # nothing to initialize
        pass

    def close(self) -> None:
        # could close requests.Session in the future
        pass

    def dump_state(self) -> Dict[str, Any]:
        return {
            "session_type": self.session_type,
            "env": self.env,
            "base_url": self.client.base_url,
            "metadata": self.metadata.copy(),
        }

    def get(self, *args, **kwargs): return self.client.get(*args, **kwargs)
    def post(self, *args, **kwargs): return self.client.post(*args, **kwargs)
    def put(self, *args, **kwargs): return self.client.put(*args, **kwargs)
    def delete(self, *args, **kwargs): return self.client.delete(*args, **kwargs)
