# influx2prom

A Python CLI tool that converts InfluxDB query results to Prometheus format - without requiring an InfluxDB connection.

## Features

- Convert JSON data from InfluxDB queries to Prometheus exposition format
- Include original query in the output as a comment
- Process CSV files containing metrics data 
- Support for all Prometheus metric types (counter, gauge, histogram, summary)
- Automatic handling of labels and timestamps

## Installation

### From Source

1. Clone this repository:
```bash
git clone https://github.com/yourusername/influx2prom.git
cd influx2prom
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Convert Query Results

Convert InfluxDB query results to Prometheus format:

```bash
influx2prom query-convert \
  --query "from(bucket: \"my_bucket\") |> range(start: -1h)" \
  --data '@examples/sample-data.json' \
  --name system_cpu_usage \
  --type gauge \
  --value-column _value \
  --help-text "CPU usage in percent" \
  --label-columns host,cpu \
  --timestamp-column _time
```

You can also provide the data directly as a JSON string:

```bash
influx2prom query-convert \
  --query "from(bucket: \"my_bucket\") |> range(start: -1h)" \
  --data '[{"host":"server1", "cpu":"cpu0", "_value":45.2, "_time":"2023-05-08T12:00:00Z"}]' \
  --name system_cpu_usage \
  --type gauge \
  --value-column _value \
  --help-text "CPU usage in percent" \
  --label-columns host,cpu \
  --timestamp-column _time
```

### Convert Raw Data

Convert JSON data to Prometheus format without including a query:

```bash
influx2prom convert \
  --data '@examples/sample-data.json' \
  --name system_cpu_usage \
  --type gauge \
  --value-column _value \
  --help-text "CPU usage in percent" \
  --label-columns host,cpu \
  --timestamp-column _time
```

### Process CSV Files

Process a CSV file and convert it to Prometheus format:

```bash
influx2prom csv \
  --file examples/data/cpu.csv \
  --name system_cpu_usage \
  --type gauge \
  --value-column usage \
  --help-text "CPU usage in percent" \
  --label-columns host,cpu \
  --timestamp-column timestamp
```

## Example Data Formats

### JSON Data

JSON data should be an array of objects:

```json
[
  {
    "host": "server1",
    "cpu": "cpu0",
    "_value": 45.2,
    "_time": "2023-05-08T12:00:00Z"
  },
  {
    "host": "server1",
    "cpu": "cpu1",
    "_value": 32.5,
    "_time": "2023-05-08T12:00:00Z"
  }
]
```

### CSV File

CSV files should have headers corresponding to the columns being used:

```csv
timestamp,host,cpu,usage
2023-05-08T12:00:00Z,server1,cpu0,45.2
2023-05-08T12:00:00Z,server1,cpu1,32.5
```

## Output Format

The tool outputs metrics in the [Prometheus exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/):

```
# Query: from(bucket: "my_bucket") |> range(start: -1h)

# HELP system_cpu_usage CPU usage in percent
# TYPE system_cpu_usage gauge
system_cpu_usage{cpu="cpu0",host="server1"} 45.2 1683547200000
system_cpu_usage{cpu="cpu1",host="server1"} 32.5 1683547200000
```

## Options

For all commands, you can specify an output file with the `--output` option:

```bash
influx2prom query-convert ... --output metrics.prom
```

If no output file is specified, the result is printed to stdout.

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Format code
black .
isort .

# Type checking
mypy .
```

## License

MIT