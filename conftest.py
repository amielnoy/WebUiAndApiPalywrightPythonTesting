from __future__ import annotations

from dotenv import load_dotenv

from infra.api_session import APISession

import os
import pytest
import allure

from infra.mobile_session import MobileSession
from infra.streaming_validator import StreamingValidator


@pytest.fixture(scope="function")
def mobile_session():
    platform = os.getenv("NANIT_PLATFORM", "ios").lower()
    streaming_validator = StreamingValidator()
    session = MobileSession(platform, streaming_validator)

    with allure.step(f"Launch app on platform: {platform}"):
        session.launch_app()
        allure.attach(
            platform,
            name="Mobile Platform",
            attachment_type=allure.attachment_type.TEXT,
        )

    yield session

    with allure.step("Close app session"):
        session.close_app()


@pytest.fixture(scope="function")
def api_streaming(load_env):
    base_url = os.getenv("BASE_URL_STREAMING")
    if not base_url:
        raise RuntimeError("BASE_URL_STREAMING is not set. Please configure it in your environment or .env file.")
    return APISession(base_url)


@pytest.fixture(scope="function", autouse=True)
def load_env():
    load_dotenv()
