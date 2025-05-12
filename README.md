# influx2prom

A command-line tool to convert InfluxDB query results to Prometheus format and translate InfluxDB queries (both Flux and InfluxQL) to PromQL.

## Installation

```bash
# Clone the repository
git clone https://github.com/chaoskyle/influx2prom.git
cd influx2prom

# Install dependencies and the tool
pip install -e .
```

## Usage

influx2prom has two main commands:
- `convert`: Convert InfluxDB query results to Prometheus format
- `translate`: Translate InfluxDB queries (Flux or InfluxQL) to PromQL

```bash


# Translate a Flux query to PromQL
influx2prom translate --query "from(bucket:\"mybucket\") |> range(start: -1h) |> filter(fn: (r) => r._measurement == \"cpu\" and r._field == \"usage_user\")"

# Translate an InfluxQL query to PromQL
influx2prom translate --query "SELECT mean(\"usage_user\") FROM \"cpu\" WHERE time >= now() - 1h GROUP BY time(1m)" --type influxql
```

### Common Options

- `--output`: Output file (default: stdout)

### Convert Command Options

- `--url`: InfluxDB URL (e.g., http://localhost:8086)
- `--token`: InfluxDB API token
- `--org`: InfluxDB organization
- `--query`: Flux query to execute
- `--query-file`: File containing a Flux query (alternative to --query)
- `--input-json`: Read data from a JSON file instead of querying InfluxDB

### Translate Command Options

- `--query`: InfluxDB query to translate (Flux or InfluxQL)
- `--query-file`: File containing an InfluxDB query (alternative to --query)
- `--type`: Force query type interpretation, either 'flux' or 'influxql' (default: auto-detect)

## Examples

### Converting InfluxDB Data to Prometheus Format

Query InfluxDB and print results in Prometheus format:

```bash
influx2prom convert --url http://localhost:8086 --token YOUR_TOKEN --org YOUR_ORG --query "from(bucket:\"mybucket\") |> range(start: -1h) |> filter(fn: (r) => r._measurement == \"cpu\")"
```

Save results to a file:

```bash
influx2prom convert --url http://localhost:8086 --token YOUR_TOKEN --org YOUR_ORG --query-file query.flux --output metrics.prom
```

### Translating InfluxDB Queries to PromQL

#### Translating Flux Queries

Translate a Flux query to PromQL and print to stdout:

```bash
influx2prom translate --query "from(bucket:\"system\") |> range(start: -1h) |> filter(fn: (r) => r._measurement == \"cpu\" and r._field == \"usage_user\")"
```

Save translation to a file:

```bash
influx2prom translate --query-file flux_query.flux --output promql_query.txt
```

#### Translating InfluxQL Queries

Translate an InfluxQL query to PromQL:

```bash
influx2prom translate --query "SELECT mean(\"usage_user\") FROM \"cpu\" WHERE time >= now() - 1h GROUP BY time(1m)" --type influxql
```

Read from a file and save translation to another file:

```bash
influx2prom translate --query-file influxql_query.sql --type influxql --output promql_query.txt
```

## Example Output

Here's an example of InfluxDB data converted to Prometheus format:

### InfluxDB CSV Format:
```
_time,_measurement,_field,_value,host,region
2023-01-01T06:00:00Z,cpu,usage_user,90.5,server01,us-west
2023-01-01T07:00:00Z,cpu,usage_system,91.2,server01,us-west
2023-01-01T06:30:00Z,memory,used_percent,75.3,server01,us-west
```

### Converted to Prometheus Format:
```
cpu_usage_user{host="server01",region="us-west"} 90.5 1672552800000
cpu_usage_system{host="server01",region="us-west"} 91.2 1672556400000
memory_used_percent{host="server01",region="us-west"} 75.3 1672554600000
```

## Quick Test

To verify the tool works without an actual InfluxDB instance, run the included sample test:

```bash
python sample_test.py
```

This will demonstrate the conversion from InfluxDB CSV format to Prometheus format using sample data.

## License

MIT