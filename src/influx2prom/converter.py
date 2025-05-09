"""Convert InfluxDB query results to Prometheus format."""
import json
from typing import Any, Dict, List, Optional, Union


class PrometheusMetric:
    """Representation of a Prometheus metric."""

    def __init__(
        self,
        name: str,
        value: float,
        metric_type: str,
        labels: Optional[Dict[str, str]] = None,
        help_text: Optional[str] = None,
        timestamp: Optional[int] = None,
    ) -> None:
        """Initialize a Prometheus metric.

        Args:
            name: Name of the metric
            value: Metric value
            metric_type: Type of metric (counter, gauge, histogram, summary)
            labels: Labels for the metric
            help_text: Help text for the metric
            timestamp: Optional timestamp in milliseconds
        """
        self.name = name
        self.value = value
        self.type = metric_type
        self.labels = labels or {}
        self.help = help_text
        self.timestamp = timestamp

    def __repr__(self) -> str:
        """Return string representation of the metric."""
        return f"PrometheusMetric({self.name}, {self.value}, {self.type})"


class InfluxToPromConverter:
    """Convert InfluxDB query results to Prometheus format."""

    VALID_TYPES = ["counter", "gauge", "histogram", "summary"]

    def convert_data(
        self,
        data: List[Dict[str, Any]],
        metric_name: str,
        metric_type: str,
        value_column: str,
        label_columns: Optional[List[str]] = None,
        help_text: Optional[str] = None,
        timestamp_column: Optional[str] = None,
    ) -> List[PrometheusMetric]:
        """Convert data to Prometheus metrics.

        Args:
            data: List of data points
            metric_name: Name of the Prometheus metric
            metric_type: Type of the Prometheus metric
            value_column: Column containing the metric value
            label_columns: Columns to use as labels
            help_text: Help text for the metric
            timestamp_column: Column containing the timestamp

        Returns:
            List of PrometheusMetric objects

        Raises:
            ValueError: If metric_type is invalid or value is missing
        """
        if metric_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid metric type: {metric_type}. "
                f"Must be one of: {', '.join(self.VALID_TYPES)}"
            )

        metrics = []
        label_columns = label_columns or []

        for record in data:
            # Check if value column exists
            if value_column not in record:
                raise ValueError(f"Value column '{value_column}' not found in record")

            # Extract and validate value
            try:
                value = float(record[value_column])
            except (ValueError, TypeError):
                raise ValueError(
                    f"Invalid value in column '{value_column}': {record[value_column]}"
                )

            # Extract labels
            labels = {}
            for label in label_columns:
                if label in record and record[label] is not None:
                    labels[label] = str(record[label])

            # Extract timestamp if configured
            timestamp = None
            if timestamp_column and timestamp_column in record:
                timestamp_value = record[timestamp_column]
                if timestamp_value is not None:
                    # Handle different timestamp formats
                    if isinstance(timestamp_value, (int, float)):
                        timestamp = int(timestamp_value)
                    else:
                        # Try to parse as ISO timestamp
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(
                                str(timestamp_value).replace("Z", "+00:00")
                            )
                            timestamp = int(dt.timestamp() * 1000)
                        except (ValueError, TypeError, AttributeError):
                            # Skip timestamp if we can't parse it
                            pass

            # Create metric
            metric = PrometheusMetric(
                name=metric_name,
                value=value,
                metric_type=metric_type,
                labels=labels,
                help_text=help_text,
                timestamp=timestamp,
            )
            metrics.append(metric)

        return metrics

    def format_metrics(self, metrics: List[PrometheusMetric]) -> str:
        """Format metrics as Prometheus exposition format.

        Args:
            metrics: List of PrometheusMetric objects

        Returns:
            Formatted metrics as string
        """
        if not metrics:
            return ""

        lines = []
        # Group metrics by name and type
        metric_groups = {}
        for metric in metrics:
            key = f"{metric.name}:{metric.type}"
            if key not in metric_groups:
                metric_groups[key] = []
            metric_groups[key].append(metric)

        # Format each group
        for key, group in metric_groups.items():
            first_metric = group[0]
            
            # Add HELP comment if available
            if first_metric.help:
                lines.append(f"# HELP {first_metric.name} {first_metric.help}")
            
            # Add TYPE comment
            lines.append(f"# TYPE {first_metric.name} {first_metric.type}")
            
            # Add metrics
            for metric in group:
                # Format labels if any
                labels_str = ""
                if metric.labels:
                    labels_parts = []
                    for k, v in sorted(metric.labels.items()):
                        # Escape special characters in label values
                        escaped_value = (
                            str(v)
                            .replace("\\", "\\\\")
                            .replace('"', '\\"')
                            .replace("\n", "\\n")
                        )
                        labels_parts.append(f'{k}="{escaped_value}"')
                    labels_str = f"{{{','.join(labels_parts)}}}"
                
                # Format value with timestamp if available
                if metric.timestamp is not None:
                    lines.append(
                        f"{metric.name}{labels_str} {metric.value} {metric.timestamp}"
                    )
                else:
                    lines.append(f"{metric.name}{labels_str} {metric.value}")
            
            # Add blank line between metric groups
            lines.append("")
        
        return "\n".join(lines)