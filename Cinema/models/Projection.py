from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from .Hall import Hall
from .Movie import Movie
from .Time import Time


class Projection(models.Model):
    hall = models.ForeignKey(Hall, blank=False, null=True, on_delete=models.SET_NULL)
    movie = models.ForeignKey(Movie, blank=False, null=False, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, blank=False, null=True, on_delete=models.CASCADE)
    monetary_cost = models.DecimalField(default=20, decimal_places=2, max_digits=8,
                                        validators=[MinValueValidator(0)])
    partner_points_cost = models.DecimalField(default=20, decimal_places=2, max_digits=8,
                                              validators=[MinValueValidator(0)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.movie.name} in {self.hall} at {self.time.beginning_time}"

    def clean(self):
        if Projection.objects.filter(time=self.time, hall=self.hall).count() != 0:
            raise ValidationError("The same hall can't display more than one movie at the same time")

    class Meta:
        unique_together = [["hall", "movie"], ["hall", "time"], ["movie", "time"]]
