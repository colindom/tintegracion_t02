from django.urls import include, path
from rest_framework import routers
from spotify import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('artists', views.ArtistList.as_view(), name = "artists"),
    path('artists/<str:pk>', views.ArtistDetail.as_view(), name = "artist"),
    path('albums', views.AlbumList.as_view(), name = "albums"),
    path('albums/<str:pk>', views.AlbumDetail.as_view(), name = "album"),
    path('tracks', views.TrackList.as_view(), name = "tracks"),
    path('artists/<str:pk>/albums', views.ArtistAlbumList.as_view(), name = "artist_albums"),
    path('artists/<str:pk>/tracks', views.ArtistTrackList.as_view(), name= 'artist_tracks'),
    path('albums/<str:pk>/tracks', views.AlbumTrackList.as_view(), name='album_tracks'),
    path('tracks/<str:pk>', views.TrackDetail.as_view(), name='track'),
]