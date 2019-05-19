from django.db import models


class Starship(models.Model):
    name = models.CharField(max_length=255)
    starship_class = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)

    length = models.FloatField()
    hyperdrive_rating = models.FloatField()
    cargo_capacity = models.BigIntegerField()

    crew = models.IntegerField()
    passengers = models.IntegerField()

    def __str__(self):
        return f'<starship_class>={self.starship_class}'


class Listing(models.Model):
    name = models.CharField(max_length=255)
    ship_type = models.ForeignKey(Starship, related_name='listings')
    price = models.IntegerField()
    time_submitted = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()


    def __str__(self):
        return f'<name>={self.name}, <price>={self.price}'