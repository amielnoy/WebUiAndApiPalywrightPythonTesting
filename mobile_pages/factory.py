from infra.mobile_session import MobileSession

from mobile_pages.android_pages.android_login_page import AndroidLoginPage
from mobile_pages.android_pages.android_welcome_page import AndroidWelcomePage
from mobile_pages.android_pages.android_live_streaming_page import AndroidLiveStreamPage

from mobile_pages.ios_pages.ios_login_page import IOSLoginPage
from mobile_pages.ios_pages.ios_welcome_page import IOSWelcomePage
from mobile_pages.ios_pages.ios_live_stream_page import IOSLiveStreamPage

# -------------------- Factory functions --------------------
def get_welcome_page(session: MobileSession):
    if session.platform == "ios":
        return IOSWelcomePage(session)
    elif session.platform == "android":
        return AndroidWelcomePage(session)
    raise ValueError(f"Unsupported platform: {session.platform}")


def get_login_page(session: MobileSession):
    if session.platform == "ios":
        return IOSLoginPage(session)
    elif session.platform == "android":
        return AndroidLoginPage(session)
    raise ValueError(f"Unsupported platform: {session.platform}")


def get_live_stream_page(session: MobileSession):
    if session.platform == "ios":
        return IOSLiveStreamPage(session)
    elif session.platform == "android":
        return AndroidLiveStreamPage(session)
    raise ValueError(f"Unsupported platform: {session.platform}")
