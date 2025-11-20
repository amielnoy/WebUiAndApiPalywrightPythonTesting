from infra.mobile_session import MobileSession


class AndroidLiveStreamPage:
    def __init__(self, session: MobileSession):
        self.session = session

    def is_visible(self) -> bool:
        return self.session.is_visible("live_stream_container_android")

    def get_stream_status(self) -> str:
        return self.session.get_text("stream_status_label_android")
