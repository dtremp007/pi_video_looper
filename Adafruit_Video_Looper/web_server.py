from flask import Flask, render_template, request, jsonify
from Adafruit_Video_Looper.model import Movie
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# This will be set from the main script
video_looper = None

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

def run_flask(looper, host='0.0.0.0', port=5000):
    global video_looper
    video_looper = looper
    app.run(host=host, port=port)
