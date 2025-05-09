#!/bin/bash

# Example command to convert a query result to Prometheus format
influx2prom query-convert \
  --query "from(bucket: \"my_bucket\") |> range(start: -1h) |> filter(fn: (r) => r._measurement == \"cpu\")" \
  --data "@examples/sample-data.json" \
  --name system_cpu_usage \
  --type gauge \
  --value-column _value \
  --help-text "CPU usage in percent" \
  --label-columns host,cpu \
  --timestamp-column _time