from django.db import models
from django.core.validators import MinValueValidator

from .Actor import Discount
from .Projection import Projection
from .Hall import Seat


class Entry(models.Model):

    projection = models.ForeignKey(Projection, blank=False, null=True, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, blank=False, null=True, on_delete=models.SET_NULL)
    discounts = models.ManyToManyField(Discount, db_index=True)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.projection) + str(self.seat)

    class Meta:
        unique_together = ["projection", "seat"]

    @classmethod
    def create(cls, projection, seat, reserved):

        entry = cls(projection=projection, seat=seat, reserved=reserved)
        return entry
