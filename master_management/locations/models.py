from django.db import models


class Timezone(models.Model):
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT
    )
    time_zone = models.ForeignKey(
        Timezone, on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(
        State, on_delete=models.PROTECT
    )
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Address(models.Model):
    address_line_1 = models.CharField(max_length=500)
    address_line_2 = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=10)
    city = models.ForeignKey(
        City, on_delete=models.PROTECT
    )
    state = models.ForeignKey(
        State, on_delete=models.PROTECT
    )
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.address_line_1

