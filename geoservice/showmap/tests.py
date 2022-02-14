import os
from django.test import TestCase

from geoservice.showmap.core import CsvReader


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geoservice.geoservice.settings")
test_list1 = [{'address': 'г Майкоп', 'postal_code': '385000', 'country': 'Россия', 'federal_district': 'Южный', 'region_type': 'Респ', 'region': 'Адыгея', 'area_type': '', 'area': '', 'city_type': 'город', 'city': 'Майкоп', 'settlement_type': '', 'settlement': '', 'kladr_id': '100000100000', 'fias_id': '8cfbe842-e803-49ca-9347-1ef90481dd98', 'fias_level': '4', 'capital_marker': '2', 'okato': '79401000000', 'oktmo': '79701000001', 'tax_office': '105', 'timezone': 'UTC+3', 'geo_lat': '44.6098268', 'geo_lon': '40.1006606', 'population': '144055', 'foundation_year': '1857'}]


class CoreTestCase(TestCase):
    def test_read_file(self):
        """тестирование корректного чтения данных из CSV-файла"""
        self.assertEqual(CsvReader.read_file('test.csv'), test_list1)




