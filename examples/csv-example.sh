#!/bin/bash

# Example command to convert a CSV file to Prometheus format
influx2prom csv \
  --file examples/data/cpu.csv \
  --name system_cpu_usage \
  --type gauge \
  --value-column usage \
  --help-text "CPU usage in percent" \
  --label-columns host,cpu \
  --timestamp-column timestamp