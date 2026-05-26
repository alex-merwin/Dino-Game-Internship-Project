import pygame
import random

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
is_playing = True  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

score = 0
egg_scored = False
egg_speed = 5

sky_egg_active = False
sky_egg_scored = False
sky_egg_speed = 7
sky_egg_rect = pygame.Rect(0, 0, 0, 0)

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)

# Load sprite assets
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(random.randint(850, 1100), GROUND_Y))
sky_egg_rect = egg_surf.get_rect(midtop=(-100, -100))


while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                player_rect.bottomleft = (25, GROUND_Y)
                egg_rect.left = random.randint(850, 1100)
                egg_speed = random.randint(5, 8)
                sky_egg_active = False
                sky_egg_rect.top = -100
                score = 0
                egg_scored = False
                sky_egg_scored = False

    if is_playing:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_rect.x += 5
            if player_rect.right > 800:
                player_rect.right = 800
        else:
            if player_rect.left > 25:
                player_rect.x -= 2

        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        
        score_surf = game_font.render(f"Score: {score}", False, "Black")
        score_rect = score_surf.get_rect(center=(400, 50))
        pygame.draw.rect(screen, "#c0e8ec", score_rect)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        screen.blit(score_surf, score_rect)

        # Adjust egg's horizontal location then blit it
        egg_rect.x -= egg_speed
        if egg_rect.right <= 0:
            egg_rect.left = random.randint(800, 1050)
            egg_speed = random.randint(5, 9)
            egg_scored = False
            
            
                
        screen.blit(egg_surf, egg_rect)

        

        if egg_rect.right < player_rect.left and not egg_scored:
            score += 1
            egg_scored = True

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        # When player collides with enemy, game ends
        if egg_rect.colliderect(player_rect) or (sky_egg_active and sky_egg_rect.bottom >= 0 and sky_egg_rect.colliderect(player_rect)):
            is_playing = False

    # When game is over, display game over message
    else:
        screen.fill("black")
        
        game_over_surf = game_font.render(f"Game Over! Final Score: {score}", False, "White")
        game_over_rect = game_over_surf.get_rect(center=(400, 200))
        screen.blit(game_over_surf, game_over_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()