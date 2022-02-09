import csv
import operator
from math import radians, cos, sin, sqrt
from abc import ABC
import numpy
import folium
from scipy.spatial import KDTree
from dadata import Dadata
from datadata_config import configuration


class CsvReader(ABC):
    """
    Предназначен для чтения данных из CSV файла
    """
    @staticmethod
    def read_file(path):
        """
        Читает данные из CSV файла, возвращает данные в виде словаря
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
    """Предназначен для создания карты с центром в заданной точке"""
    token = configuration['API-ключ']
    secret = configuration['Секретный ключ']

    def __init__(self, adress):
        """
        Создает экземпляр класса Mapper
        :param adress: - адрес на карте, тип - str
        """
        self.adress = adress

    def create_map(self, geocoder=Dadata):
        """
        Создает карту, с центом в точке с адресом, указанным в
        параметре экземпляра self.adress
        :param geocoder: - класс, используемый для геокодирования
        данных, по умолчанию - Dadata
        :return: объект-карту класса folium.Map
        """
        with geocoder(self.token, self.secret) as dadata:
            address_info = dadata.clean(name="address", source=self.adress)
            lat = address_info['geo_lat']
            lon = address_info['geo_lon']
            coordinates = [lat, lon]
            new_map = folium.Map(location=coordinates,
                                 zoom_start=13)
            folium.Marker(
                location=coordinates,
                popup=address_info['result']).add_to(new_map)
            return new_map


if __name__ == '__main__':
    map1 = Mapper('Сочи').create_map()
    map1.save('new_map.html')

