import os

from django.test import TestCase

from geoservice.showmap.core import CsvReader, Transform

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geoservice.geoservice.settings")
test_list1 = [{'address': 'г Майкоп', 'postal_code': '385000', 'country': 'Россия', 'federal_district': 'Южный', 'region_type': 'Респ', 'region': 'Адыгея', 'area_type': '', 'area': '', 'city_type': 'город', 'city': 'Майкоп', 'settlement_type': '', 'settlement': '', 'kladr_id': '100000100000', 'fias_id': '8cfbe842-e803-49ca-9347-1ef90481dd98', 'fias_level': '4', 'capital_marker': '2', 'okato': '79401000000', 'oktmo': '79701000001', 'tax_office': '105', 'timezone': 'UTC+3', 'geo_lat': '44.6098268', 'geo_lon': '40.1006606', 'population': '144055', 'foundation_year': '1857'}]
test_tuple1 = (3481.3856464692303, 2931.667530646146, 4459.717259060366)


class CoreTestCase(TestCase):
    def test_read_file(self):
        """тестирование корректного чтения данных из CSV-файла"""
        self.assertEqual(test_list1, CsvReader.read_file('test.csv'))

    def test_geodetic2ecef(self):
        """тестирование корректного преобразования координат"""
        result = Transform.geodetic2ecef(float(test_list1[0]['geo_lat']),
                                         float(test_list1[0]['geo_lon']))
        self.assertEqual(test_tuple1, result)




