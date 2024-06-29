from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from Adafruit_Video_Looper.model import Movie, Playlist
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# This will be set from the main script
video_looper = None

# USB drive mount path from video_looper.ini
USB_DRIVE_PATH = '/mnt/usbdrive0'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    video_looper._playbackStopped = False
    movie = video_looper._playlist.get_next(video_looper._is_random, video_looper._resume_playlist)
    if movie:
        video_looper._player.play(movie)
    return jsonify({"status": "playing"})

@app.route('/pause')
def pause():
    video_looper._player.pause()
    return jsonify({"status": "paused"})

@app.route('/stop')
def stop():
    video_looper._playbackStopped = True
    video_looper._player.stop(3)
    return jsonify({"status": "stopped"})

@app.route('/next')
def next_video():
    video_looper._playlist.seek(1)
    video_looper._player.stop(3)
    return jsonify({"status": "next video"})

@app.route('/queue', methods=['POST'])
def queue_video():
    video_path = request.json['path']
    video_looper._playlist.add(Movie(video_path, os.path.basename(video_path), 1))
    return jsonify({"status": "video queued"})

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(USB_DRIVE_PATH, filename)
            try:
                # Save the file to the USB drive
                file.save(file_path)

                # Get the current list of movies
                current_movies = video_looper._playlist._movies

                # Add the new movie to the list
                new_movie = Movie(file_path, filename, 1)
                current_movies.append(new_movie)

                # Recreate the playlist with the updated list of movies
                video_looper._playlist = Playlist(current_movies)

                return redirect(url_for('index'))
            except Exception as e:
                app.logger.error(f"Error saving file: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
    return '''
    <!doctype html>
    <title>Upload new Video</title>
    <h1>Upload new Video</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def run_flask(looper, host='0.0.0.0', port=5000):
    global video_looper
    video_looper = looper
    app.run(host=host, port=port)
