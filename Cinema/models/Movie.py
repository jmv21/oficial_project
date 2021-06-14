from django.db import models
from django.core.validators import MinValueValidator
from IS_Project.settings import MEDIA_URL, STATIC_URL



class Movie(models.Model):

    name = models.CharField(max_length=50)

    nationality = models.CharField(max_length=50)

    genre = models.CharField(max_length=50)

    views = models.IntegerField(default=0,validators=[MinValueValidator(0)])

    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    poster = models.ImageField(default='/movie_pics/default.jpg', upload_to='profile_pics/', null=True, blank=True)

    synopsis = models.TextField(default="It's a movie", max_length=250)

    def __str__(self):
        return self.name

    def get_image(self):
        if self.poster:
            return '{}{}'.format(MEDIA_URL, self.poster)
        return '{}{}'.format(STATIC_URL, 'media/default.jpg')

