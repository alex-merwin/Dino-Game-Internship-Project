import pygame
import random
from operator import itemgetter

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True

score_file = "scores.txt"

def load_scores():
    scores = []
    try:
        file = open(score_file, "r")
        for line in file:
            line = line.strip()
            if "," in line:
                name, score_val = line.rsplit(",", 1)
                try:
                    scores.append((name, int(score_val.strip())))
                except ValueError:
                    pass
        file.close()
    except FileNotFoundError:
        pass
    scores.sort(key=itemgetter(1), reverse=True)
    return scores

def save_score(name, score_val):
    scores = load_scores()
    scores.append((name, score_val))
    scores.sort(key=itemgetter(1), reverse=True)
    file = open(score_file, "w")
    for name, score_val in scores:
        file.write(f"{name},{score_val}\n")
    file.close()

is_entering_name = False
username = ""

is_settings = False
sound_effects_vol = 50
jump_sound = pygame.mixer.Sound("audio/jump.MP3")
jump_sound.set_volume(sound_effects_vol/100)

small_font = pygame.font.Font(pygame.font.get_default_font(), 28)
mini_font = pygame.font.Font(pygame.font.get_default_font(), 18)
current_font_color = "Black"
is_playing = True
GROUND_Y = 300
JUMP_GRAVITY_START_SPEED = -15.6
players_gravity_speed = 0
can_double_jump = False
score = 0
is_paused = False
time_paused = 0
total_time_paused = 0

sky_egg_active = False
sky_egg_speed = 7
sky_egg_telegraph_timer = 0
sky_egg_telegraph_x = 0


HEART_SURF = pygame.image.load("graphics/level/heart.png").convert_alpha()
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
current_sky = SKY_SURF
GROUND_SURF_1 = pygame.image.load("graphics/level/ground.png").convert()
GROUND_SURF_2 = pygame.image.load("graphics/level/ground.png").convert()
ground_rect_1 = GROUND_SURF_1.get_rect(topleft = (800, GROUND_Y))
ground_rect_2 = GROUND_SURF_2.get_rect(topleft = (0, GROUND_Y))
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
score_surf = game_font.render("SCORE?", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))
player_size = (65,85)
runningman1 = pygame.transform.scale(pygame.image.load("graphics/player/runningman1.png").convert_alpha(),player_size)
runningman2 = pygame.transform.scale(pygame.image.load("graphics/player/runningman2.png").convert_alpha(),player_size)
runningman3 = pygame.transform.scale(pygame.image.load("graphics/player/runningman3.png").convert_alpha(),player_size)
runningman4 = pygame.transform.scale(pygame.image.load("graphics/player/runningman4.png").convert_alpha(),player_size)
player_frames = [runningman1, runningman2, runningman3, runningman4]
player_frame_index = 0
animation_speed = 10
animation_counter = 0

player_surf = runningman1
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
player_hitbox = player_rect.inflate(-32, -26)
egg_rotation_angle = 0
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))
egg_hitbox = egg_rect.inflate(-7,-7)
egg_width = egg_surf.get_width()
is_double_egg = False

sky_egg_surf = pygame.transform.scale(egg_surf, (egg_surf.get_width() * 2, egg_surf.get_height() * 2))
sky_egg_rect = sky_egg_surf.get_rect(midtop=(-100, -100))

lives = 3
is_invincible = False
invincible_timer = 0
invincible_duration = 90

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_UP
                or event.type == pygame.MOUSEBUTTONDOWN
            ):
                jump_sound.play()
                if player_rect.bottom >= GROUND_Y:
                    players_gravity_speed = JUMP_GRAVITY_START_SPEED
                    can_double_jump = True
                elif can_double_jump:
                    players_gravity_speed = JUMP_GRAVITY_START_SPEED
                    can_double_jump = False
            elif is_playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if is_settings:
                            is_settings = False
                        else:
                            is_paused = not is_paused
                            if is_paused:
                                time_paused = pygame.time.get_ticks()
                            else:
                                total_time_paused += pygame.time.get_ticks() - time_paused

                    elif event.key == pygame.K_s and is_paused:
                        is_settings = not is_settings

                    elif event.key == pygame.K_q and is_paused and not is_settings:
                        running = False

                    elif is_settings:
                        if event.key == pygame.K_LEFT:
                            sound_effects_vol = max(0, sound_effects_vol - 5)
                            jump_sound.set_volume(sound_effects_vol / 100)
                        elif event.key == pygame.K_RIGHT:
                            sound_effects_vol = min(100, sound_effects_vol + 5)
                            jump_sound.set_volume(sound_effects_vol / 100)
        else:
            if is_entering_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username.strip():
                        save_score(username.strip(), score)
                        is_entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.unicode.isprintable() and len(username) < 15:
                        username += event.unicode
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_playing = True
                    lives = 3
                    is_invincible = False
                    egg_rect.left = 800
                    sky_egg_active = False
                    sky_egg_rect.top = -100
                    sky_egg_telegraph_timer = 0
                    player_rect.bottomleft = (25, GROUND_Y)
                    score = 0
                    time_paused = 0
                    total_time_paused = 0
                    username = ""

    if is_playing:
        if not is_paused:
            time_paused = 0
            screen.fill("purple")
            screen.blit(current_sky, (0, 0))
            ground_rect_1.x -= 5
            ground_rect_2.x -= 5
            if ground_rect_1.right < 0:
                ground_rect_1.left = ground_rect_2.right
            if ground_rect_2.right < 0:
                ground_rect_2.left = ground_rect_1.right
            screen.blit(GROUND_SURF_1, ground_rect_1)
            screen.blit(GROUND_SURF_2, ground_rect_2)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_rect.x -= 5
            if keys[pygame.K_RIGHT]:
                player_rect.x += 5
            if player_rect.left < 0:
                player_rect.left = 0
            if player_rect.right > 266:
                player_rect.right = 266

            score_surf = game_font.render(f"Score: {score}", False, current_font_color)
            score_rect = score_surf.get_rect(center=(400, 50))
            screen.blit(score_surf, score_rect)

            egg_speed = 5 + min(score // 15, 10)
            egg_rect.x -= egg_speed
            if egg_rect.right <= 0:
                score += 1
                if is_double_egg:
                    score += 1
                egg_rect.left = 800
                is_double_egg = random.random() < 0.21

            egg_rotation_angle = (egg_rotation_angle + egg_speed * 1.4) % 360
            rotated_egg = pygame.transform.rotate(egg_surf, egg_rotation_angle)
            rotated_rect = rotated_egg.get_rect(center=egg_rect.center)
            screen.blit(rotated_egg, rotated_rect)

            if is_double_egg:
                second_center = (egg_rect.centerx + egg_width, egg_rect.centery)
                screen.blit(rotated_egg, rotated_egg.get_rect(center=second_center))
                egg_hitbox = pygame.Rect(0, 0, (egg_width * 2) - 4, egg_rect.height - 4)
                egg_hitbox.center = (egg_rect.centerx + (egg_width / 2), egg_rect.centery)
            else:
                egg_hitbox = pygame.Rect(0, 0, egg_width - 4, egg_rect.height - 4)
                egg_hitbox.center = egg_rect.center
            pygame.draw.rect(screen, "red", egg_hitbox, 2)

            if not sky_egg_active and sky_egg_telegraph_timer == 0 and random.random() < 0.01:
                sky_egg_telegraph_timer = 40
                sky_egg_telegraph_x = random.randint(0, 266 - sky_egg_surf.get_width())

            if sky_egg_telegraph_timer > 0:
                sky_egg_telegraph_timer -= 1
                if (sky_egg_telegraph_timer // 5) % 2 == 0:
                    pygame.draw.rect(screen, "red", (sky_egg_telegraph_x, 0, sky_egg_surf.get_width(), 400), 2)
                if sky_egg_telegraph_timer == 0:
                    sky_egg_active = True
                    sky_egg_rect.x = sky_egg_telegraph_x
                    sky_egg_rect.top = -sky_egg_surf.get_height()

            if sky_egg_active:
                sky_egg_rect.y += sky_egg_speed
                screen.blit(sky_egg_surf, sky_egg_rect)
                if sky_egg_rect.top > 400:
                    score += 1
                    sky_egg_active = False
                    sky_egg_rect.top = -100

            if player_rect.bottom >= GROUND_Y:
                animation_counter += 1
                if animation_counter >= animation_speed:
                    animation_counter = 0
                    player_frame_index = (player_frame_index + 1) % len(player_frames)
                player_surf = player_frames[player_frame_index]
            else:
                player_surf
                animation_counter = 0

            players_gravity_speed += 1
            player_rect.y += players_gravity_speed
            if player_rect.bottom > GROUND_Y:
                player_rect.bottom = GROUND_Y
            screen.blit(player_surf, player_rect)
            player_hitbox.center = player_rect.center
            pygame.draw.rect(screen, "red", player_hitbox, 2)

            if (egg_hitbox.colliderect(player_hitbox) or (sky_egg_active and sky_egg_rect.colliderect(player_hitbox))) and not is_invincible:
                lives -= 1
                is_invincible = True
                invincible_timer = invincible_duration
                if sky_egg_active and sky_egg_rect.colliderect(player_hitbox):
                    sky_egg_active = False
                    sky_egg_rect.top = -100
                if lives <= 0:
                    is_playing = False
                    is_entering_name = True
                    username = ""

            if is_invincible:
                invincible_timer -= 1
                if invincible_timer <= 0:
                    is_invincible = False

            for i in range(lives):
                screen.blit(HEART_SURF, (10 + i * 50, 10))
        if is_paused:
            pause_overlay = pygame.Surface((800, 400), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 150))
            screen.blit(pause_overlay, (0, 0))
            if is_settings:
                setting_surf = game_font.render("Settings Menu", False, "white")
                screen.blit(setting_surf, setting_surf.get_rect(center=(400, 110)))
                sound_effects_vol_label = small_font.render(f"Sound Effests Volume: {sound_effects_vol}", False, "white")
                screen.blit(sound_effects_vol_label, sound_effects_vol_label.get_rect(center=(400, 195)))

                bar_x, bar_y, bar_w, bar_h = 200, 215, 400, 22
                pygame.draw.rect(screen, "gray", (bar_x, bar_y, bar_w, bar_h))
                pygame.draw.rect(screen, "white", (bar_x, bar_y, int(bar_w * sound_effects_vol / 100), bar_h))
                pygame.draw.rect(screen, "white", (bar_x, bar_y, bar_w, bar_h), 2)

                instruct_surf = mini_font.render("<- -> to adjust sound_effects_vol", False, "white")
                screen.blit(instruct_surf, instruct_surf.get_rect(center = (400,270)))


                back_surf = mini_font.render("ESC to go back to pause menu", False, "white")
                screen.blit(back_surf, back_surf.get_rect(center=(200, 380)))
            else:
                pause_surf = game_font.render("PAUSED", False, "White")
                resume_surf = small_font.render("ESC to Resume", False, "Gray")
                quit_surf = small_font.render("Q to Quit", False, "Gray")
                to_settings_surf = small_font.render("S to Settings", False, "Gray")

                screen.blit(pause_surf, pause_surf.get_rect(center=(400, 160)))
                screen.blit(resume_surf, resume_surf.get_rect(center=(400, 215)))
                screen.blit(quit_surf, quit_surf.get_rect(center=(400, 245)))
                screen.blit(to_settings_surf, to_settings_surf.get_rect(center = (400, 275)))

    else:
        screen.fill("black")
        screen.blit(game_font.render(f"Game Over! Score: {score}", False, "White"),
        game_font.render(f"Game Over! Score: {score}", False, "White").get_rect(center=(400, 80)))

        if is_entering_name:
            screen.blit(small_font.render("Enter your name:", False, "Gray"), small_font.render("Enter your name:", False, "Gray").get_rect(center=(400, 180)))
            screen.blit(game_font.render(username + "|", False, "White"), game_font.render(username + "|", False, "White").get_rect(center=(400, 240)))
            screen.blit(mini_font.render("Press ENTER to save", False, "Gray"), mini_font.render("Press ENTER to save", False, "Gray").get_rect(center=(400, 310)))
        else:
            scores = load_scores()
            for i, (name, s) in enumerate(scores[:5]):
                screen.blit(small_font.render(f"{i+1}. {name}  {s}", False, "White"),
                        small_font.render(f"{i+1}. {name}  {s}", False, "White").get_rect(center=(400, 170 + i * 36)))
            screen.blit(small_font.render("SPACE to play again", False, "Gray"), small_font.render("SPACE to play again", False, "Gray").get_rect(center=(400, 360)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()