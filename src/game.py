
import pygame
import random
import math


class GameAction(enumerate):
    Idle = 0
    Shoot = 1
    Left = 2
    Right = 3


class Game():

    def __init__(self, bullet_speed=5,
                 player_speed=2.5,
                 enemy_speed=2,

                 num_of_enemies=6):

        # settings
        self.bullet_speed = bullet_speed
        self.player_speed = player_speed
        self.enemy_speed = enemy_speed
        self.num_of_enemies = num_of_enemies

        pygame.init()

        # Create the screen
        self.screen = pygame.display.set_mode((800, 600))

        # Title and Icon
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load("images/ufo-icon.png")
        pygame.display.set_icon(icon)

        # background
        background_temp = pygame.image.load(
            "images/space-galaxy-background.jpg")
        self.background = pygame.transform.scale(background_temp, (800, 600))

        # enemy
        self.enemy_img = []
        self.enemy_x_change = []
        self.enemy_y_change = []
        self.enemy_x = []
        self.enemy_y = []

        self.reset_enemies()

        # player
        self.player_img = pygame.image.load("images/battleship.png")
        self.player_img = pygame.transform.scale(self.player_img, (64, 64))

        self.player_x_change = 0
        self.player_x = 370
        self.player_y = 500

        # bullet
        self.bullet_img = pygame.image.load("images/bullet.png")
        self.bullet_img = pygame.transform.scale(self.bullet_img, (32, 32))
        self.bullet_x_change = 0
        self.bullet_y_change = -bullet_speed
        self.bullet_x = 0
        self.bullet_y = 0
        # ready - hidden
        # fire - moving
        self.bullet_state = "ready"

        # score
        self.score_value = 0
        self.score_font = pygame.font.Font("freesansbold.ttf", 32)
        self.text_x = 10
        self.text_y = 10

        # Game over
        self.is_game_over = False
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 64)

    def reset_enemies(self):
        del self.enemy_img[:]
        del self.enemy_x_change[:]
        del self.enemy_y_change[:]
        del self.enemy_x[:]
        del self.enemy_y[:]

        for i in range(self.num_of_enemies):
            enemy_img_temp = pygame.image.load("images/ufo.png")
            self.enemy_img.append(
                pygame.transform.scale(enemy_img_temp, (64, 64)))

            self.enemy_x_change.append(self.enemy_speed)
            self.enemy_y_change.append(32)
            self.enemy_x.append(random.randint(0, 736))
            self.enemy_y.append(random.randint(50, 150))

    def show_enemy(self, x, y, index):
        self.screen.blit(self.enemy_img[index], (x, y))

    def show_player(self, x, y):
        self.screen.blit(self.player_img, (x, y))

    def show_bullet(self, x, y):
        self.screen.blit(self.bullet_img, (x, y))

    def fire_bullet(self, x, y):
        if self.bullet_state == "ready":
            self.bullet_state = "fire"
            self.bullet_x = x + 16
            self.bullet_y = y + 10
            # screen.blit(bullet_img, (x + 16, y + 10))

    def is_collision(self, enemy_x, enemy_y, bullet_x, bullet_y):
        enemy_x += 32
        enemy_y += 32
        bullet_x += 16
        distance = math.sqrt((enemy_x - bullet_x) ** 2 +
                             (enemy_y - bullet_y) ** 2)
        return distance < 32

    def show_score(self, x, y):
        score = self.score_font.render(
            f"Score: {self.score_value}", True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def show_game_over(self):
        game_over = self.game_over_font.render(
            "Game Over", True, (255, 255, 255))
        self.screen.blit(game_over, (220, 250))


    def do_each_game_loop(self, action=None):

        # Red, Green, Blue
        self.screen.fill((0, 0, 0))
        # Background image
        self.screen.blit(self.background, (0, 0))

        # input {
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # key stroke {
            if event.type == pygame.KEYDOWN:
                # this only hit once even when key is kept down.
                if event.key == pygame.K_LEFT:
                    self.player_x_change = -self.player_speed
                if event.key == pygame.K_RIGHT:
                    self.player_x_change = self.player_speed
                if event.key == pygame.K_SPACE:
                    self.fire_bullet(self.player_x, self.player_y)
                if event.key == pygame.K_r:
                    self.reset()
                    self.score_value = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player_x_change = 0
            # }
        
        if not action is None:
            if (action == GameAction.Idle):
                pass
            elif (action == GameAction.Shoot):
                self.fire_bullet(self.player_x, self.player_y)
            elif (action == GameAction.Left):
                self.player_x_change = -self.player_speed
            elif (action == GameAction.Right):
                self.player_x_change = self.player_speed
        # }

        # movement
        if not self.is_game_over:
            # player movement {
            self.player_x += self.player_x_change

            # boundary check
            if self.player_x < 0:
                self.player_x = 0
            if self.player_x >= 736:
                self.player_x = 736
            # }

            # enemy movement
            for i in range(self.num_of_enemies):
                # Game over
                if self.enemy_y[i] > 400:
                    self.is_game_over = True
                    break

                self.enemy_x[i] += self.enemy_x_change[i]

                # boundary check
                if self.enemy_x[i] >= 736:
                    self.enemy_x_change[i] = -self.enemy_x_change[i]
                    self.enemy_y[i] += self.enemy_y_change[i]
                if self.enemy_x[i] < 0:
                    self.enemy_x_change[i] = -self.enemy_x_change[i]
                    self.enemy_y[i] += self.enemy_y_change[i]

            # bullet movement {
            if self.bullet_state == "fire":
                self.bullet_y += self.bullet_y_change

                # Collision
                for i in range(self.num_of_enemies):
                    if self.is_collision(self.enemy_x[i], self.enemy_y[i], self.bullet_x, self.bullet_y):
                        self.bullet_state = "ready"
                        self.score_value += 1
                        # print(score_value)
                        # enemy respawn
                        self.enemy_x[i] = random.randint(0, 736)
                        self.enemy_y[i] = random.randint(50, 150)

            if self.bullet_y < -32:
                self.bullet_state = "ready"
            # }

        # render {
        if self.bullet_state == "fire":
            self.show_bullet(self.bullet_x, self.bullet_y)
        self.show_player(self.player_x, self.player_y)
        self.show_score(self.text_x, self.text_y)
        for i in range(self.num_of_enemies):
            self.show_enemy(self.enemy_x[i], self.enemy_y[i], i)
        if (self.is_game_over):
            self.show_game_over()

        pygame.display.update()
        # }

        return True


    def run_game(self):

        # Game loop
        is_running = True
        while is_running:
            is_running = self.do_each_game_loop()


    def reset(self):
        # enemy
        self.reset_enemies()

        # player
        self.player_x_change = 0
        self.player_x = 370
        self.player_y = 500

        # bullet
        self.bullet_x_change = 0
        self.bullet_y_change = -self.bullet_speed
        self.bullet_x = 0
        self.bullet_y = 0
        # ready - hidden
        # fire - moving
        self.bullet_state = "ready"

        # score
        self.score_value = 0

        # Game over
        self.is_game_over = False


if __name__ == "__main__":
    # pixels per frame
    bullet_speed = 5
    player_speed = 2.5
    enemy_speed = 2
    num_of_enemies = 6
    game = Game(bullet_speed,
                player_speed,
                enemy_speed,
                num_of_enemies)
    game.run_game()
