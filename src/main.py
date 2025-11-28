from time import time
import pygame
import os
from src import process_song_folder
from src import input_handler
from src import music_player
from src import metronome
from src import assign_map_values
import threading

def main():
    # Initialize pygame
    print("started")
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

    # Use repository root as base so data folders at project root are found
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    song_data_folder = process_song_folder.SongProcessor().parse_sayovortex_file(os.path.join(base_path, "data", "song_folder", "SongFolder1", "testSong1.txt"))
    # create map
    assign_map_values(song_data_folder)
    song_path = song_data_folder["General"].get("AudioFilename")
    song_lead_in = song_data_folder["General"].get("AudioLeadIn")
    song_title = song_data_folder["Metadata"].get("Title")
    song_artist = song_data_folder["Metadata"].get("Artist")
    song_creator = song_data_folder["Metadata"].get("Creator")
    song_version = song_data_folder["Metadata"].get("Version")
    print(f"Loaded song: {song_title} by {song_artist} [{song_version}], mapped by {song_creator}")
    print(f"Audio file: {song_path}, Lead-in: {song_lead_in}ms")

    map_loader_instance = map_loader.AssignMapValues(song_data_folder)

    player = music_player.MusicPlayer(os.path.join(base_path, "data", "song_folder", "SongFolder1", song_path))
    player.play()

    metronome_instance = metronome.Metronome(160, 4)
    metronome_thread = threading.Thread(target=metronome_instance.start, daemon=True)
    metronome_thread.start()

    # Main game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_str = key_map.get(event.key)
                print(f"Current position: {player.get_position():.3f} seconds", end='\r')
                if key_str:
                    input_handler.is_key_pressed(key_str)
        
        # Handle held keys
        keys = pygame.key.get_pressed()
        input_handler.is_key_held(keys)

        # Cap the framerate
        clock.tick(60)
    
    # Clean up
    pygame.quit()

if __name__ == '__main__':
    main()