class DummyMovie:
    def __init__(self, target, title=None, repeats=1):
        self.target = target
        self.title = title
        self.repeats = repeats
        self.playcount = 0

    def was_played(self):
        self.playcount += 1

    def clear_playcount(self):
        self.playcount = 0

class DummyPlaylist:
    def __init__(self):
        self._movies = [DummyMovie("dummy_path1.mp4", "Dummy Title 1"),
                        DummyMovie("dummy_path2.mp4", "Dummy Title 2")]
        self._index = 0

    def get_next(self, is_random, resume=False):
        return self._movies[self._index]

    def seek(self, amount):
        self._index = (self._index + amount) % len(self._movies)

    def set_next(self, path):
        # Mock setting the next movie
        pass

class DummyVideoLooper:
    def __init__(self):
        self._playbackStopped = True
        self._playlist = DummyPlaylist()
        self._is_random = False
        self._resume_playlist = False
        self._reader = DummyReader()
        self._player = DummyPlayer()

class DummyReader:
    def __init__(self):
        self._mounter = DummyMounter()

    def search_paths(self):
        return ['./var/usbdrive0', './var/usbdrive0']

class DummyMounter:
    def search_paths(self):
        return ['./var/usbdrive0', './var/usbdrive0']

class DummyPlayer:
    def play(self, movie):
        print(f"Playing movie: {movie.target}")

    def pause(self):
        print("Pausing movie")

    def stop(self, timeout):
        print("Stopping movie")
