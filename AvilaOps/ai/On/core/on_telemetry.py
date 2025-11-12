from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

OTEL_ENDPOINT = "http://localhost:4317"

resource = Resource(attributes={SERVICE_NAME: "avilaops-on"})

trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_ENDPOINT, insecure=True)))
trace.set_tracer_provider(trace_provider)

metric_exporter = OTLPMetricExporter(endpoint=OTEL_ENDPOINT, insecure=True)
reader = PeriodicExportingMetricReader(metric_exporter)
metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))

tracer = trace.get_tracer("on.core")
meter = metrics.get_meter("on.core")
