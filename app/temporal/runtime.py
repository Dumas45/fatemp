from temporalio.runtime import PrometheusConfig, Runtime, TelemetryConfig

from app.config import settings


def create_runtime() -> Runtime:
    """Temporal SDK runtime exposing worker/client metrics for Prometheus."""
    return Runtime(
        telemetry=TelemetryConfig(
            metrics=PrometheusConfig(bind_address=settings.worker_metrics_address)
        )
    )
