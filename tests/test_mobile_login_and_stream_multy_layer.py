import pytest
import allure

from conftest import api_streaming
from infra.mobile_session import MobileSession
from mobile_pages.factory import (
    get_welcome_page,
    get_login_page,
    get_live_stream_page,
)
from infra.streaming_validator import StreamMetric, StreamingValidator
from infra.allure_utils import AllureStep


@pytest.mark.parametrize(
    "email,password",
    [
        ("demo_app1@nanit.com", "12341234"),
        ("demo_app2@nanit.com", "12344321"),
    ]
)
@pytest.mark.e2e_api_integrated
@allure.feature("Mobile Streaming")
@allure.story("Login and Live Stream Status Validation")
@allure.title("Stream status are consistent between UI and backend")
def test_mobile_and_backend_stream_status_are_consistent(
    email,
    password,
    mobile_session: MobileSession,
    api_streaming,
):
    step = AllureStep("Mobile & Backend Stream Status")
    allure.dynamic.parameter("email", email)

    with step("Print base URL and test credentials (masked password)"):
        print("\nurl=" + api_streaming.client.base_url)
        print(f"Testing login with {email} / {'*' * len(password)}")
        step.attach_text("Streaming API base URL", api_streaming.client.base_url)
        step.attach_text("Test email", email)

    with step("Open Welcome page and validate visibility"):
        welcome = get_welcome_page(mobile_session)
        assert welcome.is_visible(), "Welcome screen should show login button"

    with step("Navigate from Welcome to Login screen"):
        welcome.tap_login()
        login = get_login_page(mobile_session)
        assert login.is_visible(), "Login screen should be visible after tapping login"

    with step("Fill login form and submit"):
        login.enter_email(email)
        login.enter_password(password)
        login.accept_terms()
        login.tap_login()

    with step("Validate Live Stream screen is visible and status is 'streaming' on UI"):
        live = get_live_stream_page(mobile_session)
        assert live.is_visible(), "Live Stream screen should be visible after successful login"

        ui_status = live.get_stream_status()
        step.attach_text("UI streaming status (first check)", ui_status)
        assert ui_status == "streaming", "error streaming not detected on mobile app"

    with step("Validate streaming status via backend API and compare with UI"):
        api_streaming_validator = mobile_session.api_streaming_validator
        api_streaming_validator.set_network_condition(api_streaming, "normal")

        status = api_streaming_validator.fetch_on_metric(api_streaming, StreamMetric.status)

        step.attach_text("Backend streaming status", status)
        step.attach_text("UI streaming status (before final assert)", live.get_stream_status())

        assert live.get_stream_status() == status, (
            "error streaming status is not identical in mobile ui & on streaming"
        )

    with step("Final log – Test passed"):
        msg = "Test passed: Mobile login and stream status are the same on mobile ui & on streaming."
        print(msg)
        step.attach_text("Final result", msg)
