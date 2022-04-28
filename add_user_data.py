import models
import serializers


def update_artist(artist_name, artist_data):
    song_model, ias_model, artist_model, album_model = models.song, models.info_about_song, models.artist, models.album
    errors = serializers.ArtistSchema().validate(artist_data)
    if errors:
        return errors
    artist_query = artist_model.query.add_columns(artist_model.artist_id) \
        .filter(artist_model.artist_name == artist_name.title())
    current_artist = artist_model.query.get(artist_query.artist_id)
    current_artist.artist_name = artist_data['artist_name']
    current_artist.artist_info = artist_data['artist_info']
