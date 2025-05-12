#!/usr/bin/env python3
"""
Test script to demonstrate influx2prom functionality with sample data
"""
import sys
from src.main import influx_to_prometheus
from src.influx2promql import influx_to_promql

# Sample InfluxDB CSV response (simulating what would be returned from the API)
sample_csv = """#group,false,false,true,true,false,false,true,true,true,true
#datatype,string,long,dateTime:RFC3339,dateTime:RFC3339,dateTime:RFC3339,double,string,string,string,string
#default,_result,,,,,,,,,
,result,table,_start,_stop,_time,_value,_field,_measurement,host,region
,,0,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T06:00:00Z,90.5,usage_user,cpu,server01,us-west
,,0,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T07:00:00Z,91.2,usage_system,cpu,server01,us-west
,,1,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T06:30:00Z,75.3,used_percent,memory,server01,us-west
,,1,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T07:30:00Z,78.1,used_percent,memory,server01,us-west
,,2,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T06:00:00Z,120.5,usage_user,cpu,server02,us-east
,,2,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T07:00:00Z,125.7,usage_system,cpu,server02,us-east
"""

# Sample InfluxDB queries for translation testing
sample_flux_query = 'from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage_user")'
sample_influxql_query = 'SELECT mean("usage_user") FROM "cpu" WHERE time >= now() - 1h GROUP BY time(1m)'

def main():
    print("== Sample InfluxDB CSV Data ==")
    print(sample_csv)

    print("\n== Converted to Prometheus Format ==")
    # Convert the sample data to Prometheus format
    prometheus_data = influx_to_prometheus(sample_csv)
    print(prometheus_data)

    print("\n== Testing InfluxDB to PromQL Translation ==")
    print("Flux query: " + sample_flux_query)
    print("Translated to PromQL: " + influx_to_promql(sample_flux_query))

    print("\nInfluxQL query: " + sample_influxql_query)
    print("Translated to PromQL: " + influx_to_promql(sample_influxql_query, 'influxql'))

    print("\n== Example Commands ==")
    print('# Convert to Prometheus format:')
    print('influx2prom convert --url http://localhost:8086 --token YOUR_TOKEN --org YOUR_ORG --query "from(bucket:\'metrics\') |> range(start: -1h) |> filter(fn: (r) => r._measurement == \'cpu\')"')

    print('\n# Translate Flux query to PromQL:')
    print('influx2prom translate --query "from(bucket:\'metrics\') |> range(start: -1h) |> filter(fn: (r) => r._measurement == \'cpu\')"')

    print('\n# Translate InfluxQL query to PromQL:')
    print('influx2prom translate --query "SELECT mean(\'usage_user\') FROM \'cpu\' WHERE time >= now() - 1h" --type influxql')

if __name__ == "__main__":
    main()