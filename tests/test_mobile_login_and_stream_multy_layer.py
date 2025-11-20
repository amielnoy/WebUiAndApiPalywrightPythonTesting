import os
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
def test_mobile_and_backend_stream_status_are_consistent(email, password, mobile_session: MobileSession, api_streaming):
    allure.dynamic.parameter("email", email)

    with allure.step("Print base URL and test credentials (masked password)"):
        print("\nurl=" + api_streaming.client.base_url)
        print(f"Testing login with {email} / {'*' * len(password)}")
        allure.attach(
            api_streaming.client.base_url,
            name="Streaming API base URL",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            email,
            name="Test email",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Open Welcome page and validate visibility"):
        welcome = get_welcome_page(mobile_session)
        assert welcome.is_visible(), "Welcome screen should show login button"

    with allure.step("Navigate from Welcome to Login screen"):
        welcome.tap_login()
        login = get_login_page(mobile_session)
        assert login.is_visible(), "Login screen should be visible after tapping login"

    with allure.step("Fill login form and submit"):
        login.enter_email(email)
        login.enter_password(password)
        login.accept_terms()
        login.tap_login()

    with allure.step("Validate Live Stream screen is visible and status is 'streaming' on UI"):
        live = get_live_stream_page(mobile_session)
        assert live.is_visible(), "Live Stream screen should be visible after successful login"
        ui_status = live.get_stream_status()
        allure.attach(
            ui_status,
            name="UI streaming status (first check)",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert ui_status == "streaming", "error streaming not detected on mobile app"

    with allure.step("Validate streaming status via backend API and compare with UI"):
        api_streaming_validator = mobile_session.api_streaming_validator
        api_streaming_validator.set_network_condition(api_streaming, "normal")

        status = api_streaming_validator.fetch_on_metric(api_streaming, StreamMetric.status)

        # Attach API status + UI status before assert
        allure.attach(
            status,
            name="Backend streaming status",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            live.get_stream_status(),
            name="UI streaming status (before final assert)",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert live.get_stream_status() == status, (
            "error streaming status is not identical in mobile ui & on streaming"
        )

    with allure.step("Final log – Test passed"):
        print("Test passed: Mobile login and stream status are the same on mobile ui & on streaming.")
        allure.attach(
            "Test passed",
            name="Final result",
            attachment_type=allure.attachment_type.TEXT,
        )
