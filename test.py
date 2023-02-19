import pygame

# Initialize Pygame and set up a window
pygame.init()
window = pygame.display.set_mode((640, 480))

# Set up a timer that triggers an event after 2 seconds
timer = pygame.time.set_timer(pygame.USEREVENT, 2000)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            print("Timer triggered at", pygame.time.get_ticks(), "ms")

    # Update the display
    window.fill((255, 255, 255))
    pygame.display.flip()

# Quit Pygame
pygame.quit()