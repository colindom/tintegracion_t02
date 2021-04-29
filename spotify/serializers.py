from spotify.models import Artist, Album, Track
from rest_framework import serializers
from base64 import b64encode
from django.urls import reverse

# Estructura de serializers tomada de https://stackoverflow.com/questions/49579116/django-rest-framework-how-to-encrypt-the-passwords-from-put-and-patch/49580453
class ArtistSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField()
    self = serializers.SerializerMethodField()

    def get_self(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(Artist.get_absolute_url(obj))

    def get_albums(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(Artist.get_absolute_url(obj)) + "/albums"
    
    def get_tracks(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(Artist.get_absolute_url(obj)) + "/tracks"

    def create(self, validated_data):
        return Artist.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        if 'artist' in validated_data:
            instance.artist.id = b64encode(validated_data.get('artist').get('name')).decode('utf-8')
            instance.user.save()
        return instance

    class Meta:
        model = Artist
        fields = ['id', 'name', 'age', 'self', 'albums', 'tracks']


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField()
    self = serializers.SerializerMethodField()

    def get_self(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(Album.get_absolute_url(obj))
    
    def get_artist(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('artist', args=[obj.artist_id]))

    def get_tracks(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(Album.get_absolute_url(obj)) + '/tracks'

    def create(self, validated_data):
        artist = self.context.get('artist')
        validated_data['artist_id'] = artist.id
        return Album.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        if '' in validated_data:
            instance.artist.id = b64encode(validated_data.get('artist').get('name')).decode('utf-8')
            instance.user.save()
        return instance

    class Meta:
        model = Album
        fields = ['id', 'name', 'genre', 'self', 'artist', 'tracks']

class TrackSerializer(serializers.ModelSerializer):
    artist = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()
    self = serializers.SerializerMethodField()

    def get_self(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(Track.get_absolute_url(obj))
    
    def get_artist(self, obj):
        request = self.context.get('request')
        album = Album.objects.get(pk=obj.album_id)
        return request.build_absolute_uri(reverse('artist', args=[album.artist_id]))
    
    def get_album(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('album', args=[obj.album_id]))

    def create(self, validated_data):
        album = self.context.get('album')
        validated_data['album_id'] = album.id
        return Track.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        if '' in validated_data:
            instance.artist.id = b64encode(validated_data.get('artist').get('name')).decode('utf-8')
            instance.user.save()
        return instance
        
    class Meta:
        model = Track
        fields = ['id', 'name', 'duration', 'times_played', 'self', 'artist', 'album']
        #fields = ['id', 'name', 'duration', 'times_played', 'artist', 'album', 'Self']