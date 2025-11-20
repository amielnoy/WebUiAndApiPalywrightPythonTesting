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

@pytest.mark.parametrize(
    "email,password",
    [
        ("demo_app1@nanit.com", "12341234"),
        ("demo_app2@nanit.com", "12344321"),
    ]
)
@pytest.mark.mobile_ui
@allure.feature("Mobile UI")
@allure.story("Login and navigate till stream status Flow")
@allure.title("mobile stream status validation for {email}")
def test_mobile_stream_status(email, password, mobile_session: MobileSession, api_streaming):
    allure.dynamic.parameter("email", email)

    with allure.step("Log test configuration and API URL"):
        print("url=" + api_streaming.client.base_url)
        print(f"Testing login with: {email} / {'*' * len(password)}")

        allure.attach(api_streaming.client.base_url, "Streaming API URL", allure.attachment_type.TEXT)
        allure.attach(email, "Login email", allure.attachment_type.TEXT)

    with allure.step("Open Welcome page and validate visibility"):
        welcome = get_welcome_page(mobile_session)
        assert welcome.is_visible(), "Welcome screen should show login button"

    with allure.step("Tap login on Welcome page"):
        welcome.tap_login()

    with allure.step("Open Login page and validate visibility"):
        login = get_login_page(mobile_session)
        assert login.is_visible(), "Login screen should be visible after tapping login"

    with allure.step("Fill login form and submit"):
        login.enter_email(email)
        login.enter_password(password)
        login.accept_terms()
        login.tap_login()

    with allure.step("Validate Live Stream screen is visible and streaming status == 'streaming'"):
        live = get_live_stream_page(mobile_session)

        assert live.is_visible(), "Live Stream screen should be visible after login"

        ui_status = live.get_stream_status()
        allure.attach(
            ui_status,
            name="UI streaming status",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert ui_status == "streaming"

    with allure.step("Final confirmation message"):
        message = "Test passed: Mobile login completed successfully and stream status = 'streaming' on mobile app."
        print(message)
        allure.attach(message, "Final Result", allure.attachment_type.TEXT)
