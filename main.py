from time import time
import pygame
import os
import input_handler
import music_player
import metronome
import threading

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Live Input Example")

running = True
clock = pygame.time.Clock()


input_handler.init_input()

key_map = {
    pygame.K_z: 'z',
    pygame.K_x: 'x',
    pygame.K_c: 'c',
    pygame.K_q: 'q',
    pygame.K_w: 'w'
}



base_path = os.path.dirname(__file__)
song_path = os.path.join(base_path, "mp3_storage", "testSong1.mp3")
player = music_player.MusicPlayer(song_path)
player.play()

metronome_instance = metronome.Metronome(160, 4)
metronome_thread = threading.Thread(target=metronome_instance.start, daemon=True)
metronome_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            key_str = key_map.get(event.key)
            print(f"Current position: {player.get_position():.3f} seconds", end='\r')

            if key_str:
                input_handler.is_key_pressed(key_str)
                

    keys = pygame.key.get_pressed()
    input_handler.is_key_held(keys)

    clock.tick(60)

    


pygame.quit()