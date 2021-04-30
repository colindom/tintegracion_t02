from spotify.models import Artist, Album, Track
from spotify.serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base64 import b64encode
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

#Código basado en el tutorial de django rest framework
#artists
class ArtistList(APIView):
    queryset = Artist.objects.all()

    @csrf_exempt
    def get(self, request, format=None):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True, context={'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @csrf_exempt
    def post(self, request, format=None):
        mrequest = request.data
        mrequest['id'] = b64encode(mrequest['name'].encode()).decode('utf-8')[:22]
        new_artist = ArtistSerializer(data=mrequest, context={'request' : request})
        if new_artist.is_valid():
            search = Artist.objects.filter(id= b64encode(new_artist.validated_data['name'].encode()).decode('utf-8'))[:22]
            if len(search) == 0:
                new_artist.save()
                return Response(new_artist.data, status=status.HTTP_201_CREATED)
            else:
                return Response(search.first(), status = status.HTTP_409_CONFLICT)
        return Response(new_artist.errors, status=status.HTTP_400_BAD_REQUEST)

#artists/<artist_id>
class ArtistDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise Http404
    
    def get_tracks(self, artist):
        tracks = Track.objects.filter(album_id__artist_id= artist)
        return tracks

    def get(self, request, pk, format=None):
        artist = self.get_object(pk)
        artist = ArtistSerializer(artist,  context={'request' : request})
        return Response(artist.data)

    def delete(self, request, pk, format=None):
        artist = self.get_object(pk)
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ArtistPlay(APIView):

    def get_object(self, pk):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        artist = self.get_object(pk)
        tracks = Track.objects.filter(album_id__artist_id= artist).update(times_played=F('times_played')+1)
        return Response(status=status.HTTP_200_OK)
#albums
class AlbumList(APIView):
    queryset = Album.objects.all()
    

    @csrf_exempt
    def get(self, request, format=None):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True, context={'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)
#albums/<album_id>
class AlbumDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        album = self.get_object(pk)
        album = AlbumSerializer(album,  context={'request' : request})
        return Response(album.data)

    def put(self, request, pk, format=None):
        album = self.get_object(pk)
        tracks = Track.objects.filter(album_id= artist).update(times_played=F('times_played')+1)
        return Response(status=status.HTTP_200_OK)


    def delete(self, request, pk, format=None):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlbumPlay(APIView):

    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        album = self.get_object(pk)
        tracks = Track.objects.filter(album_id= artist).update(times_played=F('times_played')+1)
        return Response(status=status.HTTP_200_OK)

#tracks
class TrackList(APIView):
    queryset = Track.objects.all()

    @csrf_exempt
    def get(self, request, format=None):
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True, context={'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)

#artists/<artist_id>/albums
class ArtistAlbumList(APIView):
    queryset = Album.objects.all()

    @csrf_exempt
    def get(self, request, pk, format=None):
        try:
            Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise Http404
        albums = Album.objects.filter(artist_id=pk)
        serializer = AlbumSerializer(albums, many=True, context={'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @csrf_exempt
    def post(self, request, pk, format=None):
        try:
            artist = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mrequest = request.data
        mrequest['id'] = b64encode((mrequest['name'] + ":" + artist.id).encode()).decode('utf-8')[:22]
        new_album = AlbumSerializer(data=mrequest, context={'request' : request, 'artist': artist})
        if new_album.is_valid():
            search = Album.objects.filter(id= b64encode((new_album.validated_data['name'] + ":" + artist.id).encode()).decode('utf-8'))[:22]
            if len(search) == 0:
                new_album.save()
                return Response(new_album.data, status=status.HTTP_201_CREATED)
            else:
                return Response(search.first(), status = status.HTTP_409_CONFLICT)
        return Response(new_album.errors, status=status.HTTP_400_BAD_REQUEST)

    

#artists/<artist_id>/tracks
class ArtistTrackList(APIView):
    queryset = Track.objects.all()

    @csrf_exempt
    def get(self, request, pk, format=None):
        try:
            Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise Http404
        tracks = Track.objects.filter(album_id__artist_id=pk)
        serializer = TrackSerializer(tracks, many=True, context={'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#albums/<album_id>/tracks
class AlbumTrackList(APIView):
    queryset = Track.objects.all()

    @csrf_exempt
    def get(self, request, pk, format=None):
        try:
            Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404
        tracks = Track.objects.filter(album_id=pk)
        serializer = TrackSerializer(tracks, many=True, context={'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request, pk, format=None):
        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404
        mrequest = request.data
        mrequest['id'] = b64encode((mrequest['name'] + ":" + album.id).encode()).decode('utf-8')[:22]
        new_track = TrackSerializer(data=mrequest, context={'request' : request, 'album':album})
        if new_track.is_valid():
            search = Track.objects.filter(id= b64encode((new_track.validated_data['name'] + ":" + album.id).encode()).decode('utf-8'))[:22]
            if len(search) == 0:
                new_track.save()
                return Response(new_track.data, status=status.HTTP_201_CREATED)
            else:
                return Response(search.first(), status = status.HTTP_409_CONFLICT)
        return Response(new_track.errors, status=status.HTTP_400_BAD_REQUEST)
#tracks/<track_id>

class TrackDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        track = self.get_object(pk)
        track = TrackSerializer(track,  context={'request' : request})
        return Response(track.data)

class TrackPlay(APIView):

    def put(self, request, pk, format=None):
        tracks = Track.objects.filter(id=pk).update(times_played=F('times_played')+1)
        return Response(status=status.HTTP_200_OK)