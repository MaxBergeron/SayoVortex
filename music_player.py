import pygame
import time
import threading

class MusicPlayer:
    def __init__(self, mp3_path):
        pygame.mixer.init()
        self.mp3_path = mp3_path
        self.length = 0
        self.start_time = None
        self.paused_time = 0
        self.is_playing = False

    def load(self):
        pygame.mixer.music.load(self.mp3_path)
        self.length = pygame.mixer.Sound(self.mp3_path).get_length()

    def play(self):
        self.load()
        pygame.mixer.music.play()
        self.start_time = time.time()
        self.is_playing = True

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.paused_time = self.get_position()
            self.is_playing = False

    def unpause(self):
        if not self.is_playing:
            pygame.mixer.music.unpause()
            self.start_time = time.time() - self.paused_time
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.start_time = None
        self.paused_time = 0

    def get_position(self):
        if self.is_playing and self.start_time is not None:
            return time.time() - self.start_time
        return self.paused_time

    def get_length(self):
        return self.length

# Example usage:
if __name__ == "__main__":
    mp3_file = "C:\\Users\\Maxence Bergeron\\Downloads\\SayoVortex_v1\\mp3_storage\\testSong1.mp3"  # Replace with your mp3 file path
    player = MusicPlayer(mp3_file)
    player.play()
    try:
        while player.get_position() < player.get_length():
            print(f"Current position: {player.get_position():.2f} seconds", end='\r')
            time.sleep(0.1)
    except KeyboardInterrupt:
        player.stop()
        print("\nStopped.")