from django.db import models
from base64 import b64encode
from django.urls import reverse


class Artist(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=50,  blank=False, default=None)
    age = models.IntegerField(blank=False)

    def get_absolute_url(self):
        return reverse('artist', args=[str(self.id)])

class Album(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=50,  blank=False, default=None)
    genre = models.CharField(max_length=50,  blank=False, default=None)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('album', args=[str(self.id)])

class Track(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,  blank=False, default=None)
    duration = models.FloatField(blank=False)
    times_played = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('track', args=[str(self.id)])