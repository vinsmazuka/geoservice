import csv
import operator
from math import cos, radians, sin, sqrt

import folium
import numpy
from dadata import Dadata
from scipy.spatial import KDTree

from . import datadata_config


class CsvReader:
    """
    Предназначен для чтения данных из CSV файла
    """
    @staticmethod
    def read_file(path):
        """
        Читает данные из CSV файла, возвращает данные в виде словаря
        :param path: путь к файлу(тип - str)
        """
        try:
            with open(path, 'r', newline='', encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                result = list(reader)
        except TypeError:
            return None
        else:
            return result


class Mapper:
    """
    Предназначен для создания карты с центром в заданной точке.
    """
    token = datadata_config.configuration['API-ключ']
    secret = datadata_config.configuration['Секретный ключ']
    geocoder = Dadata
    map_creator = folium.Map
    mark_creator = folium.Marker
    icon_creator = folium.Icon

    def __init__(self, address):
        """
        Создает экземпляр класса Mapper
        :param address: - адрес на карте(тип - str)
        """
        self.address = address

    def create_map(self, cities, radius=''):
        """
        Создает карту, с центом в точке с адресом, указанным в
        параметре экземпляра self.address,
        создает на карте маркеры городов в радиусе radius,
        если данный аргумент задан
        :param cities: - словарь, содержащий информацию
        о городах(тип - dict)
        :param radius: радиус в км(тип - float)
        :return: объект-карту класса folium.Map
        """
        try:
            with self.geocoder(self.token, self.secret) as dadata:
                address_info = dadata.clean(name="address", source=self.address)
                lat = address_info['geo_lat']
                lon = address_info['geo_lon']
                coordinates = [lat, lon]
                new_map = self.map_creator(location=coordinates,
                                           zoom_start=13,
                                           height='70%')
                self.mark_creator(location=coordinates,
                                  popup=address_info['result']).add_to(new_map)
        except ValueError:
            return 'введенный адрес - не корректный, или не существует'
        else:
            def radius_correct():
                """возвращает карту с маркерами городов-соседей в заданном
                радиусе от заданного адреса"""
                ecef_cities = []
                for key, value in cities.items():
                    ecef_cities.append((key, Transform.geodetic2ecef(float(value['geo_lat']),
                                                                     float(value['geo_lon']))))
                tree = KDTree(numpy.array(list(map(lambda x: x[1], ecef_cities))))
                central_point = Transform.geodetic2ecef(float(coordinates[0]),
                                                        float(coordinates[1]))
                neighbors_indexes = tree.query_ball_point([central_point], r=radius)
                if neighbors_indexes:
                    get_neighbors = operator.itemgetter(*neighbors_indexes[0])(ecef_cities)
                    neighbors = [x[0] for x in get_neighbors]
                    for key, value in cities.items():
                        if key in neighbors and key != address_info['city']:
                            self.mark_creator(location=[value['geo_lat'], value['geo_lon']],
                                              popup=key,
                                              icon=self.icon_creator(color='gray')).add_to(new_map)
                return new_map
            check_radius = str(radius and isinstance(radius, float))
            possible_values = {
                '0.0': lambda: new_map,
                '': lambda: new_map,
                'False': lambda: 'радиус должен быть целым числом, '
                                 'либо числом с плавающей точкой',
                'True': radius_correct
            }
            result = possible_values[check_radius]
            return result()


class Transform:
    """
    Класс, используемый для трансформации координат и
    расстояний.
    Атрибуты класса a, b, esq - константы,
    определенные World Geodetic System 1984 (WGS84)
    """
    a = 6378.137
    b = 6356.7523142
    esq = 6.69437999014 * 0.001

    @classmethod
    def geodetic2ecef(cls, lat, lon, alt=0):
        """
        используется для преобразования геодезических координат
        в координаты ECEF
        :param lat: широта(тип- float)
        :param lon: долгота(тип- float)
        :param alt: тип float
        :return: кортеж из
        геоцентрических координат точки - x, y, z(тип - tuple)
        """
        lat, lon = radians(lat), radians(lon)
        xi = sqrt(1 - cls.esq * sin(lat))
        x = (cls.a / xi + alt) * cos(lat) * cos(lon)
        y = (cls.a / xi + alt) * cos(lat) * sin(lon)
        z = (cls.a / xi * (1 - cls.esq) + alt) * sin(lat)
        return x, y, z

    @classmethod
    def euclidean_distance(cls, distance):
        """преобразует заданное расстояние из параметра distance
        в Евклидово расстояние
        :param distance: расстояние в КМ(тип - str)
        :return: расстояние в КМ, тип - float
        """
        try:
            2 * cls.a * sin(float(distance) / (2 * cls.b))
        except ValueError:
            return distance
        else:
            return 2 * cls.a * sin(float(distance) / (2 * cls.b))


transform_radius = Transform.euclidean_distance
