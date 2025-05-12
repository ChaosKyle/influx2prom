import unittest
from unittest.mock import patch, mock_open
import io
import sys
from src.main import format_timestamp, influx_to_prometheus

class TestInflux2Prom(unittest.TestCase):
    
    def test_format_timestamp_rfc3339(self):
        # Test RFC3339 time format
        self.assertEqual(format_timestamp("2023-01-01T12:00:00Z"), "1672574400000")
        
    def test_format_timestamp_epoch_seconds(self):
        # Test epoch seconds
        self.assertEqual(format_timestamp("1672574400"), "1672574400000")
        
    def test_format_timestamp_epoch_milliseconds(self):
        # Test epoch milliseconds
        self.assertEqual(format_timestamp("1672574400000"), "1672574400000")
    
    def test_influx_to_prometheus(self):
        # Sample InfluxDB CSV response
        csv_data = """#group,false,false,true,true,false,false,true,true,true
#datatype,string,long,dateTime:RFC3339,dateTime:RFC3339,dateTime:RFC3339,double,string,string,string
#default,_result,,,,,,,,,
,result,table,_start,_stop,_time,_value,_field,_measurement,host
,,0,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T06:00:00Z,90.5,usage_user,cpu,server01
,,0,2023-01-01T00:00:00Z,2023-01-01T12:00:00Z,2023-01-01T07:00:00Z,91.2,usage_system,cpu,server01
"""
        result = influx_to_prometheus(csv_data)
        expected = """cpu_usage_user{host="server01"} 90.5 1672552800000
cpu_usage_system{host="server01"} 91.2 1672556400000"""
        
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()