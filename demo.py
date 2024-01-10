# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
circle_radius = 30

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, circle_radius)

    x, y = screen.get_size()
    keys = pygame.key.get_pressed()
    offset = 300 * dt
    if keys[pygame.K_w]:
        player_pos.y -= offset if player_pos.y > circle_radius else (player_pos.y - circle_radius)
    if keys[pygame.K_s]:
        player_pos.y += offset if player_pos.y < (y - circle_radius) else 0
    if keys[pygame.K_a]:
        player_pos.x -= offset if player_pos.x > circle_radius else (player_pos.x - circle_radius)
    if keys[pygame.K_d]:
        player_pos.x += offset if player_pos.x < (x - circle_radius) else 0

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()