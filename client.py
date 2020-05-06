from random import randrange
from my_classes import Network, Cannon, Player
import pygame as pg
pg.init()


# draw some shit
def draw_window(players, win, side, cannons, collision, my_id):
    win.fill((255, 255, 255))

    # your score
    font = pg.font.SysFont('comicsans', 20)
    text = font.render(f'Your score is: {player.score}', 1, (0, 0, 0))
    win.blit(text, (350, 20))

    # top three score
    sort_players = list(reversed(sorted(players, key=lambda x: players[x]["score"])))
    ran = min(len(players), 3)
    for counter, i in enumerate(sort_players[:ran]):
        text = font.render(f"{counter + 1}: Player id '{players[i]['id']}', score: {players[i]['score']}.", 1, (0, 0, 0))
        win.blit(text, (320, 50 + 30 * counter))

    # draw players, if bullet hit you cross on u also
    for player_ in players:
        p = Player(players[player_]['x'], players[player_]['y'], side, players[player_]['color'], players[player_]['id'])
        pg.draw.rect(win, colors[p.color], (p.x, p.y, p.size, p.size))
        if collision and p.id == my_id:
            pg.draw.line(WIN, (0, 0, 0), (p.x, p.y), (p.x + p.size, p.y + p.size), 10)
            pg.draw.line(WIN, (0, 0, 0), (p.x, p.y + p.size), (p.x + p.size, p.y), 10)

    # draw cannon and her bullets
    pg.draw.circle(win, cannon.color, (cannon.x, cannon.y), cannon.radius)
    for cannon_ in cannons:
        pg.draw.circle(win, cannons[cannon_].bull_c, (cannons[cannon_].bull_x, cannons[cannon_].bull_y), cannons[cannon_].bull_r)


# random respawn, not in center of field
def start_pos(width, height, side):
    x = randrange(0, width - side)
    while x in range(width // 2 - 40 - side, width // 2 + 40):
        x = randrange(0, width - side)

    y = randrange(0, height - side)
    while y in range(height // 2 - 40 - side, height // 2 + 40):
        y = randrange(0, height - side)

    return x, y


# connect to server and some crappy shit
n = Network()
WIDTH = 500
HEIGHT = 500
SIDE = 40
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128), (0, 128, 128)]
myColor = randrange(0, 5)
Players, myID = n.hello(myColor, start_pos(WIDTH, HEIGHT, SIDE))
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('online move shapes')
collision = False
vel = 5
run = True
clock = pg.time.Clock()
cannon = Cannon(WIDTH // 2, HEIGHT // 2)
player = Player(Players[myID]['x'], Players[myID]['y'], SIDE, myColor, myID)

# event loop
while run:
    clock.tick(30)

    # control shit
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:    player.y -= player.vel
    if keys[pg.K_s]:    player.y += player.vel
    if keys[pg.K_a]:    player.x -= player.vel
    if keys[pg.K_d]:    player.x += player.vel

    # exit check
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # if u hittin cannon u get more scores
    if player.collision_with_circle((cannon.x, cannon.y), cannon.radius):
        player.score += 1

    # collect info bout u and ur bullet, and send it to server, then catch it back # class: Network
    data = [player.get_info(), cannon.get_cannon()]
    Players, Cannons = n.refresh(data)

    # find path for ur bullet and check for hittin u
    cannon.chase_target(player)
    for cannon_ in Cannons:
        if player.collision_with_circle((Cannons[cannon_].bull_x, Cannons[cannon_].bull_y), Cannons[cannon_].bull_r):
            collision = True

    # draw all, and delay after death
    draw_window(Players, WIN, SIDE, Cannons, collision, myID)
    pg.display.update()
    if collision:
        pg.time.delay(200)
        player.x, player.y = start_pos(WIDTH, HEIGHT, SIDE)
        collision = False

# close connection and window
n.bye_bye()
pg.quit()
