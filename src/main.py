
import pygame, random, math

# pixels per frame
bullet_speed = 5
player_speed = 2.5
enemy_speed = 2

num_of_enemies = 6


def reset_enemies():
    global enemy_img
    global enemy_x_change
    global enemy_y_change
    global enemy_x
    global enemy_y
    del enemy_img[:]
    del enemy_x_change[:]
    del enemy_y_change[:]
    del enemy_x[:]
    del enemy_y[:]

    for i in range(num_of_enemies):
        enemy_img_temp = pygame.image.load("images/ufo.png")
        enemy_img.append(pygame.transform.scale(enemy_img_temp, (64, 64)))

        enemy_x_change.append(enemy_speed)
        enemy_y_change.append(32)
        enemy_x.append(random.randint(0, 736))
        enemy_y.append(random.randint(50, 150))

def show_enemy(x, y, index):
    screen.blit(enemy_img[index], (x, y))
def show_player(x, y):
    screen.blit(player_img, (x, y))
def show_bullet(x, y):
    screen.blit(bullet_img, (x, y))
def fire_bullet(x, y):
    global bullet_state, bullet_x, bullet_y
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet_x = x + 16
        bullet_y = y + 10
        # screen.blit(bullet_img, (x + 16, y + 10))
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    enemy_x += 32
    enemy_y += 32
    bullet_x += 16
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    return distance < 32
def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))
def show_game_over():
    game_over = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over, (220, 250))



pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/ufo-icon.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("images/space-galaxy-background.jpg")
background = pygame.transform.scale(background, (800, 600))

# enemy
enemy_img = []
enemy_x_change = []
enemy_y_change = []
enemy_x = []
enemy_y = []

reset_enemies()

# player
player_img = pygame.image.load("images/battleship.png")
player_img = pygame.transform.scale(player_img, (64, 64))

player_x_change = 0
player_x = 370
player_y = 500

# bullet
bullet_img = pygame.image.load("images/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (32, 32))
bullet_x_change = 0
bullet_y_change = -bullet_speed
bullet_x = 0
bullet_y = 0
# ready - hidden
# fire - moving
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# Game over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


# Game loop
running = True
while (running):
    # Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # key stroke
        if event.type == pygame.KEYDOWN:
            # this only hit once even when key is kept down.
            if event.key == pygame.K_LEFT:
                # print("key left pressed")
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                # print("key right pressed")
                player_x_change = player_speed
            if event.key == pygame.K_SPACE:
                # print("key space pressed")
                # bullet_state = "fire"
                # bullet_y = player_y
                # bullet_x = player_x
                fire_bullet(player_x, player_y)
            if event.key == pygame.K_r:
                reset_enemies()
                score_value = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("key released")
                player_x_change = 0

    # player movement
    player_x += player_x_change
    # boundary check
    if player_x < 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736

    # enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemy_y[i] > 400:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            show_game_over()
            break


        enemy_x[i] += enemy_x_change[i]

        # boundary check
        if enemy_x[i] >= 736:
            enemy_x_change[i] = -enemy_x_change[i]
            enemy_y[i] += enemy_y_change[i]
        if enemy_x[i] < 0:
            enemy_x_change[i] = -enemy_x_change[i]
            enemy_y[i] += enemy_y_change[i]
        show_enemy(enemy_x[i], enemy_y[i], i)

    # bullet movement
    if bullet_state == "fire":
        bullet_y += bullet_y_change
        show_bullet(bullet_x, bullet_y)
    
        # Collision
        for i in range(num_of_enemies):
            if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                bullet_state = "ready"
                score_value += 1
                # print(score_value)
                # enemy respawn
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(50, 150)

    if bullet_y < -32:
        bullet_state = "ready"
    


    show_player(player_x, player_y)

    show_score(text_x, text_y)


    pygame.display.update()
