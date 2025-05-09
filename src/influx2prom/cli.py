"""Command-line interface for influx2prom."""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
import pandas as pd

from influx2prom.converter import InfluxToPromConverter
from influx2prom.csv_processor import CSVProcessor


@click.group()
@click.version_option()
def cli():
    """Convert InfluxDB query data to Prometheus format."""
    pass


@cli.command()
@click.option(
    "--data", "-d", required=True, 
    help="JSON string or file path containing the data. If it starts with '@', it's treated as a file path."
)
@click.option(
    "--name", "-n", required=True, 
    help="Prometheus metric name"
)
@click.option(
    "--type", "-t", required=True, 
    type=click.Choice(["counter", "gauge", "histogram", "summary"]),
    help="Prometheus metric type"
)
@click.option(
    "--value-column", "-v", required=True, 
    help="Column containing the metric value"
)
@click.option(
    "--help-text", "-h", 
    help="Help text for the metric"
)
@click.option(
    "--label-columns", "-l", 
    help="Comma-separated list of columns to use as labels"
)
@click.option(
    "--timestamp-column", "-ts", 
    help="Column containing the timestamp"
)
@click.option(
    "--output", "-o", 
    help="Path to write output to (stdout if not specified)"
)
def convert(
    data: str,
    name: str,
    type: str,
    value_column: str,
    help_text: Optional[str] = None,
    label_columns: Optional[str] = None,
    timestamp_column: Optional[str] = None,
    output: Optional[str] = None,
):
    """Convert data to Prometheus format.
    
    Data should be an array of objects representing InfluxDB results.
    """
    try:
        # Parse data
        if data.startswith('@'):
            # It's a file path
            file_path = data[1:]
            if not os.path.exists(file_path):
                click.echo(f"Error: Data file not found: {file_path}", err=True)
                sys.exit(1)
            with open(file_path, 'r') as f:
                data_content = f.read()
                data_records = json.loads(data_content)
        else:
            # It's a JSON string
            data_records = json.loads(data)
        
        # Ensure it's a list
        if not isinstance(data_records, list):
            click.echo("Error: Data must be a JSON array of objects", err=True)
            sys.exit(1)
        
        # Parse label columns if provided
        labels = label_columns.split(",") if label_columns else None
        
        # Create converter
        converter = InfluxToPromConverter()
        
        # Convert to Prometheus metrics
        metrics = converter.convert_data(
            data=data_records,
            metric_name=name,
            metric_type=type,
            value_column=value_column,
            label_columns=labels,
            help_text=help_text,
            timestamp_column=timestamp_column,
        )
        
        # Format metrics
        formatted = converter.format_metrics(metrics)
        
        # Write to file or stdout
        if output:
            with open(output, "w") as f:
                f.write(formatted)
            click.echo(f"Metrics written to {output}")
        else:
            click.echo(formatted)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--file", "-f", required=True, 
    help="Path to CSV file"
)
@click.option(
    "--name", "-n", required=True, 
    help="Prometheus metric name"
)
@click.option(
    "--type", "-t", required=True, 
    type=click.Choice(["counter", "gauge", "histogram", "summary"]),
    help="Prometheus metric type"
)
@click.option(
    "--value-column", "-v", required=True, 
    help="Column containing the metric value"
)
@click.option(
    "--help-text", "-h", 
    help="Help text for the metric"
)
@click.option(
    "--label-columns", "-l", 
    help="Comma-separated list of columns to use as labels"
)
@click.option(
    "--timestamp-column", "-ts", 
    help="Column containing the timestamp"
)
@click.option(
    "--output", "-o", 
    help="Path to write output to (stdout if not specified)"
)
def csv(
    file: str,
    name: str,
    type: str,
    value_column: str,
    help_text: Optional[str] = None,
    label_columns: Optional[str] = None,
    timestamp_column: Optional[str] = None,
    output: Optional[str] = None,
):
    """Process a CSV file and convert to Prometheus format."""
    try:
        # Parse label columns if provided
        labels = label_columns.split(",") if label_columns else None
        
        # Create CSV processor
        csv_processor = CSVProcessor()
        converter = InfluxToPromConverter()
        
        # Process CSV file
        metrics = csv_processor.process_csv_file(
            file_path=file,
            metric_name=name,
            metric_type=type,
            value_column=value_column,
            label_columns=labels,
            help_text=help_text,
            timestamp_column=timestamp_column,
        )
        
        # Format metrics
        formatted = converter.format_metrics(metrics)
        
        # Write to file or stdout
        if output:
            with open(output, "w") as f:
                f.write(formatted)
            click.echo(f"Metrics written to {output}")
        else:
            click.echo(formatted)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--query", "-q", required=True,
    help="InfluxDB query (will be included in output as a comment)"
)
@click.option(
    "--data", "-d", required=True,
    help="JSON string or file path containing sample data. If it starts with '@', it's treated as a file path."
)
@click.option(
    "--name", "-n", required=True,
    help="Prometheus metric name"
)
@click.option(
    "--type", "-t", required=True,
    type=click.Choice(["counter", "gauge", "histogram", "summary"]),
    help="Prometheus metric type"
)
@click.option(
    "--value-column", "-v", required=True,
    help="Column containing the metric value"
)
@click.option(
    "--help-text", "-h",
    help="Help text for the metric"
)
@click.option(
    "--label-columns", "-l",
    help="Comma-separated list of columns to use as labels"
)
@click.option(
    "--timestamp-column", "-ts",
    help="Column containing the timestamp"
)
@click.option(
    "--output", "-o",
    help="Path to write output to (stdout if not specified)"
)
def query_convert(
    query: str,
    data: str,
    name: str,
    type: str,
    value_column: str,
    help_text: Optional[str] = None,
    label_columns: Optional[str] = None,
    timestamp_column: Optional[str] = None,
    output: Optional[str] = None,
):
    """Convert sample query results to Prometheus format with the query included as a comment."""
    try:
        # Parse data
        if data.startswith('@'):
            # It's a file path
            file_path = data[1:]
            if not os.path.exists(file_path):
                click.echo(f"Error: Data file not found: {file_path}", err=True)
                sys.exit(1)
            with open(file_path, 'r') as f:
                data_content = f.read()
                data_records = json.loads(data_content)
        else:
            # It's a JSON string
            data_records = json.loads(data)
        
        # Ensure it's a list
        if not isinstance(data_records, list):
            click.echo("Error: Data must be a JSON array of objects", err=True)
            sys.exit(1)
        
        # Parse label columns if provided
        labels = label_columns.split(",") if label_columns else None
        
        # Create converter
        converter = InfluxToPromConverter()
        
        # Convert to Prometheus metrics
        metrics = converter.convert_data(
            data=data_records,
            metric_name=name,
            metric_type=type,
            value_column=value_column,
            label_columns=labels,
            help_text=help_text,
            timestamp_column=timestamp_column,
        )
        
        # Format metrics
        formatted = converter.format_metrics(metrics)
        
        # Add query as a comment at the top
        formatted = f"# Query: {query}\n\n{formatted}"
        
        # Write to file or stdout
        if output:
            with open(output, "w") as f:
                f.write(formatted)
            click.echo(f"Metrics written to {output}")
        else:
            click.echo(formatted)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for the command line interface."""
    cli()


if __name__ == "__main__":
    main()