from __future__ import annotations

from dotenv import load_dotenv

from infra.api_session import APISession

import os
import pytest

from infra.mobile_session import MobileSession
from infra.streaming_validator import StreamingValidator

try:
    import allure
except Exception:
    allure = None


def _create_mobile_session():
    platform = os.getenv("NANIT_PLATFORM", "ios").lower()
    streaming_validator = StreamingValidator()
    session = MobileSession(platform, streaming_validator)
    return platform, session


def _launch_session(session: MobileSession, platform: str):
    session.launch_app()
    if allure:
        allure.attach(
            platform,
            name="Mobile Platform",
            attachment_type=allure.attachment_type.TEXT,
        )
    else:
        print(f"[SETUP] Launch app on platform: {platform}")


def _close_session(session: MobileSession):
    session.close_app()
    if not allure:
        print("[TEARDOWN] Close app session")


@pytest.fixture(scope="function")
def mobile_session():
    platform, session = _create_mobile_session()

    if allure:
        with allure.step(f"Launch app on platform: {platform}"):
            _launch_session(session, platform)
    else:
        _launch_session(session, platform)

    yield session

    if allure:
        with allure.step("Close app session"):
            _close_session(session)
    else:
        _close_session(session)


@pytest.fixture(scope="function")
def api_streaming(load_env):
    base_url = os.getenv("BASE_URL_STREAMING")
    if not base_url:
        raise RuntimeError("BASE_URL_STREAMING is not set. Please configure it in your environment or .env file.")
    return APISession(base_url)


@pytest.fixture(scope="function", autouse=True)
def load_env():
    load_dotenv()
