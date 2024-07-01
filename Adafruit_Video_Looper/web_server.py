from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from Adafruit_Video_Looper.model import Movie, Playlist
from flask_cors import CORS
import os

app = Flask(__name__, template_folder=os.path.join(
    os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
    )

CORS(app)

# This will be set from the main script
video_looper = None


def get_first_available_usb_drive():
    if video_looper and video_looper._reader:
        usb_paths = video_looper._reader._mounter.search_paths()
        if usb_paths:
            return usb_paths[0]
    return None


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)


@app.post('/api/play')
def play():
    video_looper._playbackStopped = False
    movie = video_looper._playlist.get_next(
        video_looper._is_random, video_looper._resume_playlist)
    if movie:
        video_looper._player.play(movie)
    return jsonify({"status": "playing"})


@app.post('/api/pause')
def pause():
    video_looper._player.pause()
    return jsonify({"status": "paused"})


@app.post('/api/stop')
def stop():
    video_looper._playbackStopped = True
    video_looper._player.stop(3)
    return jsonify({"status": "stopped"})


@app.post('/api/next')
def next_video():
    video_looper._playlist.seek(1)
    video_looper._player.stop(3)
    return jsonify({"status": "next video"})


@app.route('/api/queue', methods=['POST'])
def queue_video():
    video_path = request.json['path']
    video_looper._playlist.add(
        Movie(video_path, os.path.basename(video_path), 1))
    return jsonify({"status": "video queued"})


@app.post('/api/upload')
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        usb_drive_path = get_first_available_usb_drive()
        if not usb_drive_path:
            return jsonify({"status": "error", "message": "No USB drive found"}), 500

        file_path = os.path.join(usb_drive_path, filename)
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


@app.get('/api/current_video')
def current_video():
    current_index = video_looper._playlist._index
    current_movie = video_looper._playlist._movies[current_index]
    return jsonify({
        "target": current_movie.target,
        "title": current_movie.title,
        "repeats": current_movie.repeats,
        "playcount": current_movie.playcount
    })


@app.get('/api/playlist')
def get_playlist():
    playlist = [{
        "target": movie.target,
        "title": movie.title,
        "repeats": movie.repeats,
        "playcount": movie.playcount,
    } for movie, index in video_looper._playlist._movies]
    return jsonify(playlist)


@app.route('/api/remove_video', methods=['POST'])
def remove_video():
    video_path = request.json['path']
    video_looper._playlist._movies = [
        movie for movie in video_looper._playlist._movies if movie.target != video_path]
    return jsonify({"status": "video removed"})


@app.post('/api/update')
def update_application():
    # Authentication check (implement your own authentication mechanism)
    # if not request.headers.get('Authorization') == 'Bearer your_secret_token':
    #     return jsonify({"status": "Unauthorized"}), 401

    try:
        # Trigger the update script asynchronously
        script_path = os.path.expanduser('~/update_script.sh')
        subprocess.Popen(['/bin/sh', script_path])

        # Respond immediately to the client
        response = jsonify({"status": "Update started"})
        response.status_code = 202  # Accepted
        return response

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500
    finally:
        # Exit the Flask application
        os._exit(0)


@app.route('/healthcheck')
def healthcheck():
    return jsonify({"status": "healthy"})


def run_flask(looper, host='0.0.0.0', port=5000):
    global video_looper
    video_looper = looper
    app.run(host=host, port=port)


# if __name__ == '__main__':
#     from dummy_video_looper import DummyVideoLooper
#     print('Starting Dummy Video Looper for testing.')
#     dummy_looper = DummyVideoLooper()
#     run_flask(dummy_looper, host='127.0.0.1', port=5000)
