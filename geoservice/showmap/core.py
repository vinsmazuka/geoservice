import csv
import operator
from math import radians, cos, sin, sqrt
import numpy
import folium
from scipy.spatial import KDTree
from dadata import Dadata
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

    def create_map(self, cities, radius=None):
        """
        Создает карту, с центом в точке с адресом, указанным в
        параметре экземпляра self.address,
        создает на карте маркеры городов в радиусе radius,
        если данный аргумент задан
        :param cities: - словарт, содержащий информацию
        о городах(тип - dict)
        :param radius: радиус в км(тип - float)
        :return: объект-карту класса folium.Map
        """
        if not self.address:
            return 'адрес не задан'
        else:
            try:
                with self.geocoder(self.token, self.secret) as dadata:
                    address_info = dadata.clean(name="address", source=self.address)
                    lat = address_info['geo_lat']
                    lon = address_info['geo_lon']
                    coordinates = [lat, lon]
                    new_map = self.map_creator(location=coordinates,
                                               zoom_start=13)
                    self.mark_creator(location=coordinates,
                                      popup=address_info['result']).add_to(new_map)
            except ValueError:
                return 'введенный адрес - не корректный'
            else:
                if radius is None:
                    return new_map
                elif radius == '':
                    return new_map
                elif not isinstance(radius, float):
                    return 'радиус должен быть целым числом, либо числом с плавающей точкой'
                else:
                    cities = {
                        city['city']:
                            {'geo_lat': city['geo_lat'],
                             'geo_lon': city['geo_lon'],
                             'ecef': Transform.geodetic2ecef(float(city['geo_lat']),
                                                             float(city['geo_lon']))} for city in cities}
                    ecef_cities = []
                    for key, value in cities.items():
                        ecef_cities.append((key, value['ecef']))
                    tree = KDTree(numpy.array(list(map(lambda x: x[1], ecef_cities))))
                    central_point = Transform.geodetic2ecef(float(coordinates[0]),
                                                            float(coordinates[1]))
                    result = tree.query_ball_point([central_point], r=radius)
                    cities_around = [x[0] for x in operator.itemgetter(*result[0])(ecef_cities)]
                    for key, value in cities.items():
                        if key in cities_around and key != address_info['city']:
                            self.mark_creator(location=[value['geo_lat'], value['geo_lon']],
                                              popup=key,
                                              icon=self.icon_creator(color='gray')).add_to(new_map)
                    return new_map


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


# if __name__ == '__main__':
#     adr = 'тольdsfятти'
#     new_map = Mapper(adr).create_map(cities=CsvReader.read_file('city.csv'),
#                                      radius=Transform.euclidean_distance('15,5'))
#     # new_map = Mapper(adr).create_map(cities=CsvReader.read_file('city.csv'))
#     print(new_map)
#     new_map.save('new_map.html')








