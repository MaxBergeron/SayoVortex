import pygame
import input_handler

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


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            key_str = key_map.get(event.key)
            
            input_handler.is_key_pressed(key_str)

    keys = pygame.key.get_pressed()
    input_handler.is_key_held(keys)

    clock.tick(60)

    


pygame.quit()