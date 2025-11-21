import pytest
from infra.streaming_validator import StreamingValidator, StreamMetric
from infra.allure_utils import AllureStep
import allure


@pytest.mark.streaming_api
@allure.feature("Streaming API")
@allure.story("Network Quality Impact")
@allure.title("Stream quality degradation under poor network conditions")
def test_stream_quality_degrades_under_poor_network(api_streaming):

    step = AllureStep("Streaming Quality Degradation Test")
    validator = StreamingValidator()

    with step("Set initial network condition: normal"):
        normal_network_conditions = validator.set_network_condition(api_streaming, "normal")
        step.attach_json("Normal Network Conditions", normal_network_conditions)

    with step("Fetch streaming metrics under normal network"):
        normal_status = validator.fetch_on_metric(api_streaming, StreamMetric.status)
        normal_bitrate = validator.fetch_on_metric(api_streaming, StreamMetric.bitrate)
        normal_network_status = validator.fetch_on_metric(api_streaming, StreamMetric.network_condition)
        normal_viewers_number = validator.fetch_on_metric(api_streaming, StreamMetric.viewers)

        step.attach_json("Normal Stream Metrics", {
            "status": normal_status,
            "bitrate": normal_bitrate,
            "network": normal_network_status,
            "viewers": normal_viewers_number
        })

    with step("Validate normal network metrics"):
        validator.validate_metric(normal_status, "streaming")
        validator.validate_metric(normal_bitrate, "1080p")
        validator.validate_metric(normal_network_status, "normal")

    with step("Set degraded network condition: poor"):
        poor_network_conditions = validator.set_network_condition(api_streaming, "poor")
        step.attach_json("Poor Network Conditions", poor_network_conditions)

    with step("Fetch streaming metrics under poor network"):
        poor_status = validator.fetch_on_metric(api_streaming, StreamMetric.status)
        poor_bitrate = validator.fetch_on_metric(api_streaming, StreamMetric.bitrate)
        poor_network_status = validator.fetch_on_metric(api_streaming, StreamMetric.network_condition)
        poor_viewers_number = validator.fetch_on_metric(api_streaming, StreamMetric.viewers)

        step.attach_json("Poor Stream Metrics", {
            "status": poor_status,
            "bitrate": poor_bitrate,
            "network": poor_network_status,
            "viewers": poor_viewers_number
        })

    with step("Validate metrics under poor network"):
        validator.validate_metric(poor_status, "streaming")
        validator.validate_metric(poor_bitrate, "1080p")
        validator.validate_metric(poor_network_status, "poor")

    with step("Validate degradation of network parameters"):
        validator.validate_network_parameter_degragated(
            normal_network_conditions["latency_ms"],
            poor_network_conditions["latency_ms"]
        )
        validator.validate_network_parameter_degragated(
            normal_network_conditions["jitter_ms"],
            poor_network_conditions["jitter_ms"]
        )
        validator.validate_network_parameter_degragated(
            normal_network_conditions["packet_loss"],
            poor_network_conditions["packet_loss"]
        )

    with step("Final confirmation"):
        step.attach_text("Final Status", "Network degradation validated successfully")
