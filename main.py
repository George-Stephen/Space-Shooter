import pygame
import os
import time
import random
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.font.init()
pygame.mixer.init()

player_vel = 5  # Adjust the velocity as needed
lost_font = pygame.font.SysFont("sans serif", 50)
FPS = 60  # Set the desired frames per second
lives = 3

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Troopers")

RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

POWER_UP_IMG = pygame.image.load(os.path.join("assets", "power_up.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.jpg")), (WIDTH, HEIGHT))



pygame.mixer.music.load(os.path.join("assets", "background_music.wav"))
laser_sound = pygame.mixer.Sound(os.path.join("assets", "laser_sound.wav"))

pygame.mixer.music.play(-1)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            laser_sound.play()

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100, score=0,):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = score

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.score += 10
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                              self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                              self.ship_img.get_width() * (self.health / self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)}

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class PowerUp:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def main():
    running = True 
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("sans serif", 20)
    lost_font = pygame.font.SysFont("sans serif", 70)
    score_font = pygame.font.SysFont("sans serif", 50)
    player_vel = 5
    enemies = []
    enemy_vel = 1
    laser_vel = 5
    wave_length = 10
    player = Player(300, 650)
    power_up_vel = 5  # Velocity of the power-up
    power_up = None  # Initialize power-up as None
    power_up_timer = 10 # Timer to control the appearance of the power-up

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        score_label = main_font.render(f"score: {player.score}", 1, (255, 255, 255))

        # WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)
        
        if power_up:
            power_up.draw(WIN)  # Draw the power-up

        if lost:
            lost_label = lost_font.render("GAME OVER!!!", 1, (255, 255, 255))
            final_score = score_font.render(f"Your final score: {player.score}", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
            WIN.blit(final_score,(WIDTH / 2 - lost_label.get_width() / 2, 450))

        pygame.display.update()

    while running:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                running = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 3
            power_up_timer = pygame.time.get_ticks()  # Reset the power-up timer
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
            
        # Check if it's time to create the power-up
        if pygame.time.get_ticks() - power_up_timer > 12000:  # Adjust the time (5000 milliseconds = 5 seconds)
            power_up = PowerUp(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), POWER_UP_IMG)
            power_up_timer = pygame.time.get_ticks()  # Reset the power-up timer

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 16 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 120) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Move and draw the power-up
        if power_up:
            power_up.move(power_up_vel)
            power_up.draw(WIN)

            # Check for collisions with the player
            if power_up.collision(player):
                player.health = min(player.health + 50, player.max_health)
                power_up = None  # Reset power-up after player collects it

        player.move_lasers(-laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("sans serif", 50)
    sound_font = pygame.font.SysFont("sans serif", 30)
    running = True
    music_playing = True
    TOGGLE_MUSIC_EVENT = pygame.USEREVENT + 1

    while running:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the ENTER button to start :", 1, (255, 255, 255))
        sound_label = sound_font.render("Press the M button to turn on or off the sound", 1, (255, 255, 255))
        menu_text = "Music: ON" if music_playing else "Music: OFF"
        menu_label = sound_font.render(menu_text, 1, (255, 255, 255))
        WIN.blit(menu_label, (WIDTH - menu_label.get_width() - 10, 10))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        WIN.blit(sound_label, (WIDTH / 2 - sound_label.get_width() / 2, 400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_m:
                    # Toggle music on 'M' key press
                    music_playing = not music_playing
                    if music_playing:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                elif event.key == pygame.K_RETURN:
                    main()
            elif event.type == TOGGLE_MUSIC_EVENT:
                # Toggle music state
                music_playing = not music_playing
                if music_playing:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                              
            
    pygame.quit()

if __name__ == "__main__":
    main_menu()