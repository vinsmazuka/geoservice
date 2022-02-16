import os

import folium

from django.test import TestCase

from geoservice.showmap.core import CsvReader, Transform, Mapper


os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "geoservice.geoservice.settings")
test_list1 = [
    {'address': 'г Майкоп',
     'postal_code': '385000',
     'country': 'Россия',
     'federal_district': 'Южный',
     'region_type': 'Респ',
     'region': 'Адыгея',
     'area_type': '',
     'area': '',
     'city_type': 'город',
     'city': 'Майкоп',
     'settlement_type': '',
     'settlement': '',
     'kladr_id': '100000100000',
     'fias_id': '8cfbe842-e803-49ca-9347-1ef90481dd98',
     'fias_level': '4',
     'capital_marker': '2',
     'okato': '79401000000',
     'oktmo': '79701000001',
     'tax_office': '105',
     'timezone': 'UTC+3',
     'geo_lat': '44.6098268',
     'geo_lon': '40.1006606',
     'population': '144055',
     'foundation_year': '1857'}]

test_tuple1 = (3481.3856464692303, 2931.667530646146, 4459.717259060366)
distance = 300.9812932522452
message1 = 'введенный адрес - не корректный, или не существует'
message2 = 'радиус должен быть целым числом, ' \
           'либо числом с плавающей точкой'

cities = {'Астана': {'geo_lat': '51.1801', 'geo_lon': '71.446'},
          'Адыгейск': {'geo_lat': '44.878414', 'geo_lon': '39.190289'},
          'Майкоп': {'geo_lat': '44.6098268', 'geo_lon': '40.1006606'},
          'Горно-Алтайск': {'geo_lat': '51.9581028', 'geo_lon': '85.9603235'},
          'Алейск': {'geo_lat': '52.4922513', 'geo_lon': '82.7793606'},
          'Барнаул': {'geo_lat': '53.3479968', 'geo_lon': '83.7798064'},
          'Ярославль': {'geo_lat': '57.6215477', 'geo_lon': '39.8977411'}}

moscow = Mapper('Москва')
error_case1 = Mapper('Мо//454%сква')


class CoreTestCase(TestCase):
    def test_read_file(self):
        """тестирование корректного чтения данных из CSV-файла"""
        self.assertEqual(test_list1, CsvReader.read_file('test.csv'))

    def test_geodetic2ecef(self):
        """тестирование корректного преобразования координат"""
        result = Transform.geodetic2ecef(float(test_list1[0]['geo_lat']),
                                         float(test_list1[0]['geo_lon']))
        self.assertEqual(test_tuple1, result)

    def test_euclidean_distance(self):
        """тестирование корректного преобразования расстояния"""
        self.assertEqual(distance, Transform.euclidean_distance(300))

    def test_create_map(self):
        """тестирование корректного создания карт"""
        map1 = moscow.create_map(cities=cities)
        map2 = moscow.create_map(cities=cities, radius='')
        error_case2 = moscow.create_map(cities=cities, radius='notdigit')
        map3 = moscow.create_map(cities=cities, radius=300.0)
        self.assertTrue(isinstance(map1, folium.Map))
        self.assertEqual([55.7540471, 37.620405], map1.location)
        self.assertEqual((100.0, '%'), map1.width)
        self.assertEqual((70.0, '%'), map1.height)
        self.assertEqual(message1, error_case1.create_map(cities=cities))
        self.assertTrue(isinstance(map2, folium.Map))
        self.assertEqual((100.0, '%'), map2.width)
        self.assertEqual((70.0, '%'), map2.height)
        self.assertEqual(message2, error_case2)
        self.assertTrue(isinstance(map3, folium.Map))
        self.assertEqual([55.7540471, 37.620405], map3.location)
        self.assertEqual((100.0, '%'), map3.width)
        self.assertEqual((70.0, '%'), map3.height)








