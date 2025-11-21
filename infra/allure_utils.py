from contextlib import contextmanager
from typing import Any, Optional, Dict

try:
    import allure
except ImportError:
    allure = None


class AllureStep:
    """
    A clean helper to use Allure steps in tests and page objects.

    Example:
        step = AllureStep("Login Flow")
        with step("Enter email"):
            page.type_email("demo@nanit.com")
        step.attach_text("Login Status", "Success")
    """

    def __init__(self, base_name: str = ""):
        self.base_name = base_name

    @contextmanager
    def __call__(self, name: str):
        """
        Allows usage like:
            with step("Click login"):
                ...
        """
        if allure:
            with allure.step(self._full(name)):
                yield
        else:
            # Allure missing → graceful fallback
            print(f"[STEP] {self._full(name)}")
            yield

    # ----------------------------------------------------------------------
    # Attachment helpers
    # ----------------------------------------------------------------------

    def attach_text(self, name: str, text: str):
        if allure:
            allure.attach(text, self._full(name), allure.attachment_type.TEXT)
        else:
            print(f"[ATTACH TEXT] {self._full(name)}: {text}")

    def attach_json(self, name: str, data: Dict[str, Any]):
        if allure:
            allure.attach(str(data), self._full(name), allure.attachment_type.JSON)
        else:
            print(f"[ATTACH JSON] {self._full(name)}: {data}")

    def attach_png(self, name: str, png_bytes: bytes):
        if allure:
            allure.attach(png_bytes, self._full(name), allure.attachment_type.PNG)
        else:
            print(f"[ATTACH PNG] {self._full(name)} (binary data omitted)")

    # ----------------------------------------------------------------------

    def _full(self, name: str) -> str:
        return f"{self.base_name}: {name}" if self.base_name else name
