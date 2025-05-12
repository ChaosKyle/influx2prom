# Example Output from influx2prom

This document shows example output from the influx2prom tool.

## Sample Run

Command:
```bash
python sample_test.py
```

Output:
```
== Sample InfluxDB CSV Data ==
#group,false,false,true,true,false,false,true,true,true,true
#datatype,string,long,dateTime:RFC3339,dateTime:RFC3339,dateTime:RFC3339,double,string,string,string,string
#default,_result,,,,,,,,,
,result,table,_start,_stop,_time,_value,_field,_measurement,host,region
,,0,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T06:00:00Z,90.5,usage_user,cpu,server01,us-west
,,0,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T07:00:00Z,91.2,usage_system,cpu,server01,us-west
,,1,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T06:30:00Z,75.3,used_percent,memory,server01,us-west
,,1,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T07:30:00Z,78.1,used_percent,memory,server01,us-west
,,2,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T06:00:00Z,120.5,usage_user,cpu,server02,us-east
,,2,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T07:00:00Z,125.7,usage_system,cpu,server02,us-east


== Converted to Prometheus Format ==
cpu_usage_user{table="0",host="server01",region="us-west"} 90.5 1672552800000
cpu_usage_system{table="0",host="server01",region="us-west"} 91.2 1672556400000
memory_used_percent{table="1",host="server01",region="us-west"} 75.3 1672554600000
memory_used_percent{table="1",host="server01",region="us-west"} 78.1 1672558200000
cpu_usage_user{table="2",host="server02",region="us-east"} 120.5 1672552800000
cpu_usage_system{table="2",host="server02",region="us-east"} 125.7 1672556400000
```

## Explanation

The influx2prom tool:
1. Takes InfluxDB data in CSV format (typically from a Flux query)
2. Extracts the measurement, field, value, timestamp, and tags
3. Converts timestamps to Prometheus format (milliseconds since epoch)
4. Creates Prometheus metric names in the format: `{measurement}_{field}`
5. Formats all tags as Prometheus labels
6. Combines everything into Prometheus exposition format

The Prometheus format can be directly used with Prometheus remote write API or saved as metrics files for scraping.

## Format Comparison

| InfluxDB Format | Prometheus Format |
|-----------------|-------------------|
| Hierarchical measurements and fields | Flat metric names with `_` separator |
| Tags stored separately | Tags converted to labels in `{}` |
| RFC3339 timestamps | Millisecond epoch timestamps |
| CSV output format | Exposition text format |