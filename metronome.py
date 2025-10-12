import time
import threading
import pygame

class Metronome:
    def __init__(self, bpm, beats_per_bar):
        self.bpm = bpm
        self.beats_per_bar = beats_per_bar
        self.running = False
        # Initialize mixer; wrap in try/except to avoid import-time errors
        try:
            pygame.mixer.init()
        except Exception:
            # In some headless environments initializing audio may fail; ignore here
            pass

    def start(self):
        self.running = True
        interval = 60.0 / self.bpm
        beat = 0
        while self.running:
            beat = (beat + 1) % self.beats_per_bar
            print(f"Beat {beat + 1}")
            # Play sound here if desired
            time.sleep(interval)

    def stop(self):
        self.running = False
