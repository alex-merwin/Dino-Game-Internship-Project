import pygame
import random
import json
import sys

class Leaderboard:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = self.load_scores()
    def load_scores(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    def save_score(self, name, score):
        self.scores.append({"name": name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:5]
        try:
            with open(self.filename, "w") as f:
                json.dump(self.scores, f, indent=4)
        except IOError:
            pass


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pygame.display.set_caption("Game Leaderboard")
running = True  

FONT = pygame.font.SysFont("Arial", 24)
TITLE_FONT = pygame.font.SysFont("Arial", 30, bold=True)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
BLACK = (20, 20, 20)

lb = Leaderboard()

def draw_leaderboard():
    title_surface = TITLE_FONT.render("TOP PLAYERS", True, GOLD)
    screen.blit(title_surface, (530, 40))
    start_y = 110
    for index, entry in enumerate(lb.scores):
        rank_text = f"{index + 1}. {entry['name']}"
        score_text = str(entry['score'])

        name_surface = FONT.render(rank_text, True, WHITE)
        score_surface = FONT.render(score_text, True, WHITE)

        screen.blit(name_surface, (480, start_y))
        screen.blit(score_surface, (700, start_y))
        start_y += 45


is_playing = True  
GROUND_Y = 300  
JUMP_GRAVITY_START_SPEED = -20  
players_gravity_speed = 0  

score = 0
egg_scored = False
egg_speed = 5

sky_egg_active = False
sky_egg_scored = False
sky_egg_speed = 7

score_saved = False
player_name = ""

SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 32)

player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(random.randint(850, 1100), GROUND_Y))
sky_egg_surf = pygame.transform.smoothscale(egg_surf, (int(egg_surf.get_width() * 1.7), int(egg_surf.get_height() * 1.8)))
sky_egg_rect = sky_egg_surf.get_rect(midtop=(-100, -100))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            if not score_saved:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name.strip() == "":
                            player_name = "Player"
                        lb.save_score(player_name, score)
                        score_saved = True
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 8 and event.unicode.isalnum():
                            player_name += event.unicode
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_playing = True
                    score_saved = False
                    player_name = ""
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
            if player_rect.right > 266:
                player_rect.right = 266
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_rect.x -= 5
            if player_rect.left < 0:
                player_rect.left = 0

        screen.fill("purple")  

        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        
        score_surf = game_font.render(f"Score: {score}", False, "Black")
        score_rect = score_surf.get_rect(center=(400, 50))
        pygame.draw.rect(screen, "#c0e8ec", score_rect)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        screen.blit(score_surf, score_rect)

        egg_rect.x -= egg_speed
        if egg_rect.right <= 0:
            egg_rect.left = random.randint(800, 1050)
            egg_speed = random.randint(5, 9)
            egg_scored = False
            
            if random.randint(1, 3) == 1 and not sky_egg_active:
                sky_egg_active = True
                sky_egg_rect.centerx = random.randint(int(sky_egg_rect.width / 2), 266 - int(sky_egg_rect.width / 2))
                sky_egg_rect.top = -150
                sky_egg_scored = False
                
        screen.blit(egg_surf, egg_rect)

        if sky_egg_active:
            if sky_egg_rect.bottom < 0:
                telegraph_surface = pygame.Surface((sky_egg_rect.width, GROUND_Y), pygame.SRCALPHA)
                telegraph_surface.fill((255, 0, 0, 80))
                screen.blit(telegraph_surface, (sky_egg_rect.left, 0))
                
                pygame.draw.polygon(screen, "Red", [
                    (sky_egg_rect.centerx, 20), 
                    (sky_egg_rect.centerx - 15, 0), 
                    (sky_egg_rect.centerx + 15, 0)
                ])

            sky_egg_rect.y += sky_egg_speed
            if sky_egg_rect.bottom >= 0:
                screen.blit(sky_egg_surf, sky_egg_rect)

            
            if sky_egg_rect.bottom >= GROUND_Y and not sky_egg_scored:
                score += 1
                sky_egg_scored = True
                
            if sky_egg_rect.top > 400:
                sky_egg_active = False

        if egg_rect.right < player_rect.left and not egg_scored:
            score += 1
            egg_scored = True

        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        if egg_rect.colliderect(player_rect) or (sky_egg_active and sky_egg_rect.bottom >= 0 and sky_egg_rect.colliderect(player_rect)):
            is_playing = False

    else:
        screen.fill(BLACK)
        
        game_over_surf = game_font.render("Game Over!", True, (255, 50, 50))
        score_surf = game_font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(game_over_surf, (50, 60))
        screen.blit(score_surf, (50, 120))
        
        if not score_saved:
            prompt_surf = FONT.render("Type Name & Press ENTER:", True, GOLD)
            name_surf = game_font.render(player_name + "|", True, WHITE)
            screen.blit(prompt_surf, (50, 200))
            screen.blit(name_surf, (50, 250))
        else:
            restart_surf = FONT.render("Press SPACE to Restart", True, (150, 150, 150))
            screen.blit(restart_surf, (50, 220))
            
        draw_leaderboard()

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
sys.exit()
