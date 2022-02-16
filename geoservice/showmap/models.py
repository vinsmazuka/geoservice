from django.db import models


class City(models.Model):
    """Представляет города"""
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    federal_district = models.CharField(max_length=100)
    region_type = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    area_type = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    city_type = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    settlement_type = models.CharField(max_length=100)
    settlement = models.CharField(max_length=100)
    kladr_id = models.CharField(max_length=100)
    fias_id = models.CharField(max_length=100)
    fias_level = models.CharField(max_length=100)
    capital_marker = models.CharField(max_length=100)
    okato = models.CharField(max_length=100)
    oktmo = models.CharField(max_length=100)
    tax_office = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    geo_lat = models.CharField(max_length=100)
    geo_lon = models.CharField(max_length=100)
    population = models.CharField(max_length=100)
    foundation_year = models.CharField(max_length=100)

    def __str__(self):
        """Возвращает строковое представление экземпляра каласса City"""
        return f'{self.city}: {self.geo_lat}, {self.geo_lon}'
