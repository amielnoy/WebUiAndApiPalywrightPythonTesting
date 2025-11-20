# infra/base_session.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseSession(ABC):
    """
    Abstract base class for any test session (mobile, API, streaming, etc).

    Subclasses must implement:
      - open()
      - close()
      - dump_state()

    Shared responsibilities:
      - env handling
      - metadata store
      - optional Allure attachment
    """

    def __init__(
        self,
        session_type: str,
        env: str = "local",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.session_type = session_type
        self.env = env
        self.metadata: Dict[str, Any] = metadata or {}

    # -------------------------------------------------
    # Abstract lifecycle hooks
    # -------------------------------------------------

    @abstractmethod
    def open(self) -> None:
        """Open / initialize the session (driver, client, service)."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Close / clean up the session."""
        raise NotImplementedError

    # -------------------------------------------------
    # Abstract: each session must describe its own state
    # -------------------------------------------------

    @abstractmethod
    def dump_state(self) -> Dict[str, Any]:
        """
        State snapshot for debugging & reporting.
        Must be implemented by subclass.
        """
        raise NotImplementedError

    # -------------------------------------------------
    # Optional helpers (shared by all subclasses)
    # -------------------------------------------------

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def attach_to_allure(self, name: Optional[str] = None) -> None:
        """Attach session state to Allure if available (safe fallback)."""
        try:
            import allure  # type: ignore
        except Exception:
            return  # No allure installed = silently skip

        content = str(self.dump_state())
        allure.attach(
            content,
            name=name or f"{self.session_type} session state",
            attachment_type=getattr(allure.attachment_type, "JSON", allure.attachment_type.TEXT),
        )
