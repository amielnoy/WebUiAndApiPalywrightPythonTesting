import pytest
from infra.streaming_validator import StreamingValidator
from infra.allure_utils import AllureStep
import allure


@pytest.mark.streaming_api
@allure.feature("Streaming API")
@allure.story("Network Quality Impact")
@allure.title("Network parameters degrade under poor conditions")
def test_network_parameters_degrade_under_poor_conditions(api_streaming):

    step = AllureStep("Network Degradation Validation")
    validator = StreamingValidator()

    with step("Set initial network condition: normal"):
        normal_network_conditions = validator.set_network_condition(api_streaming, "normal")
        step.attach_json("Normal Network Conditions", normal_network_conditions)

    with step("Set degraded network condition: poor"):
        poor_network_conditions = validator.set_network_condition(api_streaming, "poor")
        step.attach_json("Poor Network Conditions", poor_network_conditions)

    with step("Validate degradation of network parameters"):
        validator.validate_network_parameter_degraded(
            normal_network_conditions["latency_ms"],
            poor_network_conditions["latency_ms"],
            "latency_ms",
        )
        validator.validate_network_parameter_degraded(
            normal_network_conditions["jitter_ms"],
            poor_network_conditions["jitter_ms"],
            "jitter_ms",
        )
        validator.validate_network_parameter_degraded(
            normal_network_conditions["packet_loss"],
            poor_network_conditions["packet_loss"],
            "packet_loss",
        )

    with step("Final confirmation"):
        step.attach_text("Final Status", "Network parameter degradation validated successfully")
