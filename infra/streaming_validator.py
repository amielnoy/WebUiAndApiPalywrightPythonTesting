from enum import Enum
from typing import Union

from infra.globals import ApiHttpConstants


class StreamMetric(Enum):
    status = "status"
    bitrate = "bitrate"
    viewers = "viewers"
    network_condition = "network_condition"


class StreamingValidator():
    def fetch_metrics(self, api_streaming):
        """
        Fetch full streaming metrics payload in one request.

        Returns the JSON body of GET /health as a dict.
        """
        response = api_streaming.get('/health')
        assert response.status_code == ApiHttpConstants.OK, f"Failed to fetch metrics: {response.status_code}"
        return response.json()

    def fetch_on_metric(self, api_streaming, metric: Union[StreamMetric, str]):
        """
        Fetch streaming data by a given metric.

        metric can be one of:
          - StreamMetric.status / "status"
          - StreamMetric.bitrate / "bitrate"
          - StreamMetric.viewers / "viewers"
          - StreamMetric.network_condition / "network_condition"
        """
        # normalize metric to string value
        if isinstance(metric, StreamMetric):
            metric_value = metric.value
        else:
            metric_value = str(metric)

        allowed = {m.value for m in StreamMetric}
        if metric_value not in allowed:
            raise ValueError(f"Invalid metric '{metric_value}'. Allowed: {sorted(allowed)}")

        response_data = self.fetch_metrics(api_streaming)
        return response_data[metric_value]

    def set_network_condition(self, api_streaming, network_condition: str):
        response = api_streaming.put("/control/network/"+network_condition)
        assert response.status_code == ApiHttpConstants.OK, f"Failed to set network condition: {response.status_code}"
        return response.json()['settings']
    def validate_metric(self, actual_metric_value,expected_metric_value):
        assert actual_metric_value == expected_metric_value, f"Expected value to be {expected_metric_value}, got {actual_metric_value}"


    def validate_network_parameter_degraded(self, before_value, after_value, param_name: str = "parameter"):
        assert float(before_value) < float(after_value), (
            f"Expected {param_name} to increase after network degradation, "
            f"got before={before_value}, after={after_value}"
        )


    def validate_valid_viewer_number_degrated(self, viewer_number_before, viewer_number_after):
        assert int(viewer_number_before) > int(viewer_number_after) , f"Expected viewer number to decrease, got {viewer_number_before} viewers before and {viewer_number_after} viewers after"
