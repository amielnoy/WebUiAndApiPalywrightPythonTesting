from infra.mobile_session import MobileSession


class IOSLiveStreamPage:
    def __init__(self, session: MobileSession):
        self.session = session

    def is_visible(self) -> bool:
        return self.session.is_visible("live_stream_container_ios")

    def get_stream_status(self) -> str:
        return self.session.get_text("stream_status_label_ios")

