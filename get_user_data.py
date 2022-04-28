import models
import json


def all_artists():
    result = models.artist.query.add_columns(models.artist.artist_id, models.artist.artist_name,
                                             models.artist.artist_info)
    data = [dict(itm) for itm in result]
    return {'data': data, 'fff': [{'ddddd': 'dd'}]}


def all_songs():
    song_model, ias_model, artist_model = models.song, models.info_about_song, models.artist
    result = song_model.query \
        .join(ias_model, ias_model.song_id == song_model.song_id) \
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(song_model.song_id, song_model.song_name, song_model.song_year,
                     artist_model.artist_name, artist_model.artist_id)
    data = [dict(itm) for itm in result]
    return {'data': data}


def artist_data(artist_name):
    song_model, ias_model, artist_model, album_model = models.song, models.info_about_song, models.artist, models.album
    result = artist_model.query \
        .join(ias_model, ias_model.artist_id == artist_model.artist_id) \
        .join(song_model, song_model.song_id == ias_model.song_id) \
        .join(album_model, album_model.album_id == ias_model.album_id) \
        .add_columns(artist_model.artist_name, artist_model.artist_info,
                     album_model.album_id, album_model.album_name, album_model.album_year,
                     song_model.song_id, song_model.song_name, song_model.song_year) \
        .filter(artist_model.artist_name == artist_name.title())
    data = [dict(itm) for itm in result]
    return {'data': data}


def album_data(artist_name, album_name):
    song_model, ias_model, artist_model, album_model = models.song, models.info_about_song, models.artist, models.album
    result = artist_model.query \
        .join(ias_model, ias_model.artist_id == artist_model.artist_id) \
        .join(song_model, song_model.song_id == ias_model.song_id) \
        .join(album_model, album_model.album_id == ias_model.album_id) \
        .add_columns(album_model.album_id, album_model.album_name, album_model.album_year, album_model.album_info,
                     song_model.song_id, song_model.song_name, song_model.song_year,
                     artist_model.artist_name) \
        .filter(artist_model.artist_name == artist_name.title()) \
        .filter(album_model.album_name == album_name.title())
    data = [dict(itm) for itm in result]
    return {'data': data}


def song_data(artist_name, song_name):
    song_model, ias_model, artist_model, album_model = models.song, models.info_about_song, models.artist, models.album
    result = artist_model.query \
        .join(ias_model, ias_model.artist_id == artist_model.artist_id) \
        .join(song_model, song_model.song_id == ias_model.song_id) \
        .join(album_model, album_model.album_id == ias_model.album_id) \
        .add_columns(song_model.song_id, song_model.song_name, song_model.song_year,
                     artist_model.artist_name, album_model.album_name) \
        .filter(artist_model.artist_name == artist_name.title()) \
        .filter(song_model.song_name == song_name.title())
    data = [dict(itm) for itm in result]
    return {'data': data}


def search(search_word):
    song_model, ias_model, artist_model, album_model = models.song, models.info_about_song, models.artist, models.album
    result_song = song_model.query\
        .join(ias_model, ias_model.song_id == song_model.song_id)\
        .join(artist_model, artist_model.artist_id == ias_model.artist_id)\
        .add_columns(song_model.song_id, song_model.song_name, song_model.origin_lang, song_model.song_year, artist_model.artist_name) \
        .filter(song_model.song_name.like(f'%{search_word}%')).all()
    result_album = album_model.query\
        .join(ias_model, ias_model.album_id == album_model.album_id)\
        .join(artist_model, artist_model.artist_id == ias_model.artist_id) \
        .add_columns(album_model.album_id, album_model.album_name, artist_model.artist_name) \
        .filter(album_model.album_name.like(f'%{search_word}%')).all()
    result_artist = artist_model.query \
        .add_columns(artist_model.artist_name) \
        .filter(artist_model.artist_name.like(f'%{search_word}%')).all()
    data = {'song': [dict(itm) for itm in result_song],
              'album': [dict(itm) for itm in result_album],
              'artist': [dict(itm) for itm in result_artist]
              }
    return {'data': data}