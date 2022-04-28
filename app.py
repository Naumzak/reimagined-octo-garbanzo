from flask import Flask, render_template, request
from shared_db import db
import get_user_data as gud
import add_user_data
import os


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.environ.get("db_name")}'
app.config['SECRET_KEY'] = '37373892'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_string = request.form.get('search')
        data = gud.search(search_string)
        return render_template('search.html', **data)

    return render_template('index.html')
@app.route('/search')
def search():
    request_args = request.args['search_string']
    data = gud.search(request_args)
    return render_template('search.html', **data)

@app.route('/artists')
def all_artists():
    data = gud.all_artists()
    return render_template('scroll.html', **data)


@app.route('/songs')
def all_songs():
    data = gud.all_songs()
    return render_template('scroll.html', **data)


@app.route('/artist/<artist_name>', methods=['GET', 'PUT'])
def artist(artist_name):
    if request.method == 'GET':
        data = gud.artist_data(artist_name)
        return render_template('artist.html', **data)
    else:
        artist_data = request.json
        add_user_data.update_artist(artist_name, artist_data)
        db.session.commit()
        return artist_data

@app.route('/artist/<artist_name>/album/<album_name>')
def album(artist_name, album_name):
    data = gud.album_data(artist_name, album_name)
    return render_template('album.html', **data)


@app.route('/artist/<artist_name>/song/<song_name>')
def song(artist_name, song_name):
    data = gud.song_data(artist_name, song_name)
    return render_template('song.html', **data)


if __name__ == '__main__':
    app.run()
