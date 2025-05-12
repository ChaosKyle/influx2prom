import unittest
from src.influx2promql import (
    detect_query_type,
    convert_flux_to_promql,
    convert_influxql_to_promql,
    influx_to_promql
)

class TestInflux2PromQL(unittest.TestCase):
    
    def test_detect_query_type(self):
        # Test Flux query detection
        flux_query = 'from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu")'
        self.assertEqual(detect_query_type(flux_query), 'flux')
        
        # Test InfluxQL query detection
        influxql_query = 'SELECT mean("usage_user") FROM "cpu" WHERE time >= now() - 1h GROUP BY time(1m)'
        self.assertEqual(detect_query_type(influxql_query), 'influxql')
        
        # Test unknown query type
        unknown_query = 'this is not a valid query'
        self.assertEqual(detect_query_type(unknown_query), 'unknown')
    
    def test_convert_flux_to_promql_basic(self):
        # Test basic Flux query conversion
        flux_query = 'from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu")'
        promql = convert_flux_to_promql(flux_query)
        self.assertIn('cpu', promql)
        self.assertIn('[-1h]', promql)
    
    def test_convert_flux_to_promql_with_field(self):
        # Test Flux query with field filter
        flux_query = 'from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage_user")'
        promql = convert_flux_to_promql(flux_query)
        self.assertIn('cpu_usage_user', promql)
        self.assertIn('[-1h]', promql)
    
    def test_convert_flux_to_promql_with_tags(self):
        # Test Flux query with tag filters
        flux_query = 'from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage_user" and r.host == "server01")'
        promql = convert_flux_to_promql(flux_query)
        self.assertIn('cpu_usage_user{host="server01"}', promql)
    
    def test_convert_flux_to_promql_with_aggregation(self):
        # Test Flux query with aggregation
        flux_query = 'from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage_user") |> mean()'
        promql = convert_flux_to_promql(flux_query)
        self.assertIn('avg(cpu_usage_user', promql)
    
    def test_convert_influxql_to_promql_basic(self):
        # Test basic InfluxQL query conversion
        influxql_query = 'SELECT "usage_user" FROM "cpu" WHERE time >= now() - 1h'
        promql = convert_influxql_to_promql(influxql_query)
        self.assertIn('cpu_usage_user', promql)
    
    def test_convert_influxql_to_promql_with_aggregation(self):
        # Test InfluxQL query with aggregation
        influxql_query = 'SELECT mean("usage_user") FROM "cpu" WHERE time >= now() - 1h GROUP BY time(1m)'
        promql = convert_influxql_to_promql(influxql_query)
        self.assertIn('avg(cpu_usage_user', promql)
    
    def test_convert_influxql_to_promql_with_tags(self):
        # Test InfluxQL query with tag filters
        influxql_query = 'SELECT "usage_user" FROM "cpu" WHERE time >= now() - 1h AND "host" = \'server01\''
        promql = convert_influxql_to_promql(influxql_query)
        self.assertIn('cpu_usage_user{host="server01"}', promql)
    
    def test_influx_to_promql_auto_detect(self):
        # Test auto-detection of query type
        flux_query = 'from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu")'
        influxql_query = 'SELECT "usage_user" FROM "cpu" WHERE time >= now() - 1h'
        
        # Should detect Flux
        promql_flux = influx_to_promql(flux_query)
        self.assertIn('cpu', promql_flux)
        
        # Should detect InfluxQL
        promql_influxql = influx_to_promql(influxql_query)
        self.assertIn('cpu_usage_user', promql_influxql)
    
    def test_influx_to_promql_force_type(self):
        # Test forcing query type
        query = 'SELECT "usage_user" FROM "cpu"'  # Basic InfluxQL
        
        # Force as InfluxQL (correct)
        promql_influxql = influx_to_promql(query, 'influxql')
        self.assertIn('cpu_usage_user', promql_influxql)
        
        # Force as Flux (incorrect but should try to parse)
        promql_flux = influx_to_promql(query, 'flux')
        # We don't assert specific content because it may not parse correctly,
        # but it shouldn't throw an exception

if __name__ == '__main__':
    unittest.main()