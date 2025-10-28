from __future__ import annotations

import shutil
from urllib import request

import allure
from _pytest.fixtures import FixtureRequest
from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page

from api_tests.api_client import APIClient

import os
from pathlib import Path
import pytest

# ----- make test outcome available on fixtures -----
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)  # rep_setup / rep_call / rep_teardown


@pytest.fixture
def page(request, browser, tmp_path_factory):
    """Playwright page with:
       - trace recorded, saved only on failure
       - last screenshot + exception attached on failure
       - video kept only on failure
    """
    videos_dir = tmp_path_factory.mktemp("videos")
    traces_dir = tmp_path_factory.mktemp("traces")

    context = browser.new_context(
        record_video_dir=str(videos_dir),
        record_video_size={"width": 1280, "height": 720},
    )
    # start tracing early so we capture as much as possible
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    yield page

    failed = bool(getattr(request.node, "rep_call", None) and request.node.rep_call.failed)

    # optional Allure
    allure = None
    try:
        import allure  # type: ignore
    except Exception:
        pass

    # 1) last screenshot on failure
    if failed:
        try:
            png = page.screenshot(full_page=True)
            if allure:
                allure.attach(png, name="Last screenshot", attachment_type=allure.attachment_type.PNG)
            else:
                out = Path("artifacts"); out.mkdir(exist_ok=True)
                (out / f"{request.node.name}__last.png").write_bytes(png)
        except Exception:
            pass

        # 2) exception/traceback text
        try:
            longrepr = getattr(request.node.rep_call, "longreprtext", None) or str(request.node.rep_call.longrepr)
            if allure:
                allure.attach(longrepr, name="Exception", attachment_type=allure.attachment_type.TEXT)
            else:
                out = Path("artifacts"); out.mkdir(exist_ok=True)
                (out / f"{request.node.name}__exception.txt").write_text(longrepr)
        except Exception:
            pass

    # 3) stop tracing (save only on failure)
    trace_path = Path(traces_dir) / f"{request.node.name}.zip"
    try:
        if failed:
            context.tracing.stop(path=str(trace_path))
        else:
            context.tracing.stop()  # discard trace to save space
    except Exception:
        trace_path = None

    # 4) close context to flush video file
    try:
        context.close()
    except Exception:
        pass

    # 5) attach (or persist) trace + video on failure
    try:
        if failed and trace_path and trace_path.exists():
            if allure:
                allure.attach.file(str(trace_path), name="trace.zip", extension=".zip")
            else:
                out = Path("artifacts"); out.mkdir(exist_ok=True)
                shutil.copy2(trace_path, out / f"{request.node.name}__trace.zip")
    except Exception:
        pass

    try:
        video = getattr(page, "video", None)
        if video:
            vpath = Path(video.path())  # valid after close()
            if failed:
                if allure and vpath.exists():
                    atype = getattr(allure.attachment_type, "WEBM", getattr(allure.attachment_type, "MP4"))
                    allure.attach.file(str(vpath), name="Test video", attachment_type=atype)
            else:
                if vpath.exists():
                    vpath.unlink(missing_ok=True)
    except Exception:
        pass




@pytest.fixture(scope="session")
def api_json_placeholder():
    return APIClient(os.getenv('BASE_URL_API_JPH'))

@pytest.fixture(scope="session")
def api_json_dummy():
    return APIClient(os.getenv('BASE_URL_API_JSON_DUMMY'))

@pytest.fixture(scope='session',autouse=True)
def base_url_fe(load_env):
    return os.getenv('BASE_URL_FE')

@pytest.fixture(scope='session',autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(autouse=True)
def attach_playwright_results(page: Page, request: FixtureRequest):
    """Fixture to perform teardown actions and attach results to Allure report
    on failure.

    Args:
        page (Page): Playwright page object.
        request: Pytest request object.

    """
    yield
    if request.node.rep_call.failed:
        allure.attach(
            body=page.url,
            name="URL",
            attachment_type=allure.attachment_type.URI_LIST,
        )
        allure.attach(
            page.screenshot(full_page=True),
            name="Screen shot on failure",
            attachment_type=allure.attachment_type.PNG,
        )
# @pytest.fixture(scope="session")
# def browser_type_launch_args():
#     return {
#         "headless": False,
#         "slow_mo": 250  # מאט את הפעולות כדי שתוכל לראות מה קורה
#     }