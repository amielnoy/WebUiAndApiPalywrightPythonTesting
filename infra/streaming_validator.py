from infra.globals import ApiHttpConstants


class StreamingValidator():
    def fetch_metrics(self, api_streaming):
        """
        Fetch full streaming metrics payload in one request.

        Returns the JSON body of GET /health as a dict.
        """
        response = api_streaming.get('/health')
        assert response.status_code == ApiHttpConstants.OK, f"Failed to fetch metrics: {response.status_code}"
        return response.json()

    def set_network_condition(self, api_streaming, network_condition: str):
        response = api_streaming.put("/control/network/"+network_condition)
        assert response.status_code == ApiHttpConstants.OK, f"Failed to set network condition: {response.status_code}"
        return response.json()['settings']
    def validate_metric(self, actual_metric_value, expected_metric_value):
        assert actual_metric_value == expected_metric_value, (
            f"Expected value to be {expected_metric_value}, got {actual_metric_value}"
        )


    def validate_network_parameter_degraded(self, before_value, after_value, param_name: str = "parameter"):
        assert float(before_value) < float(after_value), (
            f"Expected {param_name} to increase after network degradation, "
            f"got before={before_value}, after={after_value}"
        )
