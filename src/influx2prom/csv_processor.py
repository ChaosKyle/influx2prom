"""Process CSV files and convert to Prometheus format."""
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from influx2prom.converter import InfluxToPromConverter, PrometheusMetric


class CSVProcessor:
    """Process CSV files and convert to Prometheus metrics."""

    def __init__(self) -> None:
        """Initialize CSV processor."""
        self.converter = InfluxToPromConverter()

    def process_csv_file(
        self,
        file_path: str,
        metric_name: str,
        metric_type: str,
        value_column: str,
        label_columns: Optional[List[str]] = None,
        help_text: Optional[str] = None,
        timestamp_column: Optional[str] = None,
    ) -> List[PrometheusMetric]:
        """Process a CSV file and convert to Prometheus metrics.

        Args:
            file_path: Path to the CSV file
            metric_name: Name of the Prometheus metric
            metric_type: Type of the Prometheus metric
            value_column: Column containing the metric value
            label_columns: Columns to use as labels
            help_text: Help text for the metric
            timestamp_column: Column containing the timestamp

        Returns:
            List of PrometheusMetric objects

        Raises:
            FileNotFoundError: If the CSV file does not exist
            ValueError: For invalid data or configuration
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        # Read CSV into DataFrame
        df = pd.read_csv(file_path)
        
        # Check required columns
        if value_column not in df.columns:
            raise ValueError(f"Value column '{value_column}' not found in CSV file")
        
        if label_columns:
            for label in label_columns:
                if label not in df.columns:
                    raise ValueError(f"Label column '{label}' not found in CSV file")
        
        if timestamp_column and timestamp_column not in df.columns:
            raise ValueError(f"Timestamp column '{timestamp_column}' not found in CSV file")
        
        # Convert DataFrame to list of dictionaries
        records = df.to_dict(orient="records")
        
        # Convert to Prometheus metrics
        return self.converter.convert_data(
            data=records,
            metric_name=metric_name,
            metric_type=metric_type,
            value_column=value_column,
            label_columns=label_columns,
            help_text=help_text,
            timestamp_column=timestamp_column,
        )