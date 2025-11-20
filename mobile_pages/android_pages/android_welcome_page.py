from infra.mobile_session import MobileSession


class AndroidWelcomePage:
    def __init__(self, session: MobileSession):
        self.session = session

    def is_visible(self) -> bool:
        return self.session.is_visible("login_button_android")

    def tap_login(self):
        self.session.click("login_button_android")
