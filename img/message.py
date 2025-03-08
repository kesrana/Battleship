import pygame
from constant import black, green, blue, gray, yellow, bottom_panel, screen_width, screen_height, white

# next stage: buying, setting UI and dataclass preparing

# ... (all the imports and constants)
screen = pygame.display.set_mode((screen_width, screen_height))
panel = pygame.image.load('panel.png').convert_alpha()
sgrid = pygame.image.load('3x3.png').convert_alpha()
egrid = pygame.image.load('3x3.png').convert_alpha()
radar = pygame.image.load('radar.png').convert_alpha()
exp = pygame.image.load('exp.png').convert_alpha()
fire = pygame.image.load('fire.png').convert_alpha()
background_img = pygame.image.load('sea.png').convert_alpha()

# Define enemy ships and load their images
enemy_ships = ["etank", "Mothership"]  # Update the names as needed
ship_prices = {"etank": 100, "Mothership": 200}
ship_images = {ship: pygame.image.load(f'{ship}/0.png').convert_alpha() for ship in enemy_ships}

# Define current ship index
current_ship_index = 0
    
# Board set up
enemylist = [None] * 9
mylist = [None] * 9
money = 0


def get_next_ship(current_index):
    next_index = (current_index + 1) % len(enemy_ships)
    return enemy_ships[next_index], next_index
def draw_next_ship(screen, ship_name):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Next Ship: {ship_name}', True, (255, 255, 255))
    screen.blit(text, (screen_width - 280, 10))
    screen.blit(ship_images[ship_name], (screen_width - 285, 20))
def draw_money():
    money_info = f'CURRENT MONEY: $ {money}'
    myFont = pygame.font.SysFont("Times New Roman", 32)
    moneyDisplay = myFont.render(str(money_info), 1, black)
    screen.blit(moneyDisplay, (30, 30))
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
def draw_bg():
    screen.blit(background_img, (0, 0))
def draw_grid():
    screen.blit(sgrid, (600, 500))
    screen.blit(egrid, (600, 0))
def draw_panel():
    screen.blit(panel, (0, 300))
def draw_radar():
    screen.blit(radar, (1300, 0))
def draw_exp(x, y):
    screen.blit(exp, (x, y))
def draw_fire(x, y):
    screen.blit(fire, (x, y))
def draw_ship_icons():
    y = 350
    for ship_name, ship_image in ship_images.items():
        screen.blit(ship_image, (10, y))
        font = pygame.font.SysFont(None, 24)
        price_text = font.render(f'Price: ${ship_prices[ship_name]}', True, (255, 255, 255))
        screen.blit(price_text, (70, y + 80))
        y += 140

class Ship():
    def __init__(self, x, y, name, max_hp, atk, type, gauge, max_gauge):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        img = pygame.image.load(f'{self.name}/Idel/{0}.png')
        img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
        self.image = img
        self.rect = self.image.get_rect()
        self.type = type
        self.x = x
        self.y = y
        self.rect.center = (x, y)
        self.gauge = gauge
        self.max_gauge = max_gauge

    # group parameter, previous: long parameter list
    def attack(self):
        # k =1 player unit, k= 2 enemy unit
        if self.x == 680:
            i = 0
        elif self.x == 800:
            i = 1
        elif self.x == 920:
            i = 2
        # this unit is player
        if self.y > 400:
            k = 1
        # this unit is computer
        elif self.y < 400:
            k = 2
        # info = f'ship {self.name} at column {i} is initiating an attack'
        # print(info)
        a = 0
        if k == 1:
            if self.type == 'tank' or 'player':
                for z in range(3):
                    if enemylist[z + i * 3] is not None:
                        if enemylist[z + i * 3].hp > 0:
                            a = z + i * 3
                            # print("pos")
                            # print(a)
                            break
                if a == 0:
                    for z in range(9):
                        if enemylist[z] is not None:
                            if enemylist[z].hp > 0:
                                a = z
                                # print("bos")
                                # print(a)
                                break
        if k == 2:
            if self.type == 'tank' or 'player':
                for z in range(3):
                    if mylist[z + i * 3] is not None:
                        if mylist[z + i * 3].hp > 0:
                            a = z + i * 3
                            # print("pos")
                            # print(a)
                            break
                if a == 0:
                    for z in range(9):
                        if mylist[z] is not None:
                            if mylist[z].hp > 0:
                                a = z
                                # print("bos")
                                # print(a)
                                break
        damage = self.atk
        if k == 1:
            # print("enemylist index")
            # print(a)
            if enemylist[a] is not None:
                enemylist[a].hp -= damage
                if enemylist[a].hp <= 0:
                    enemylist[a].alive = False
                    if enemylist[a].type != 'aMothership':
                        print("+money")
                        global money
                        money += 50
                        print(money)
                draw_exp(enemylist[a].x, enemylist[a].y)

        if k == 2:
            # print("mylist index")
            # print(a)
            if mylist[a] is not None:
                mylist[a].hp -= damage
                if mylist[a].hp <= 0:
                    mylist[a].alive = False
                # if enemylist[i].type is not 'Mothership':
                #    print("+money")
                #    global money
                #    money += 50
                #    print(money)
                draw_exp(mylist[a].x, mylist[a].y)
        # elif self.name == 'eMothership' or 'Mothership'

    def draw(self):
        screen.blit(self.image, self.rect)
        if self.alive == False:
            draw_fire(self.x, self.y)

    def drawbar(self):
        ratio = self.hp / self.max_hp
        gratio = self.gauge / self.max_gauge
        pygame.draw.rect(screen, gray, (self.x - 55, self.y + 50, 100, 10))
        pygame.draw.rect(screen, green, (self.x - 55, self.y + 50, 100 * ratio, 10))
        pygame.draw.rect(screen, gray, (self.x - 55, self.y + 60, 100, 10))
        pygame.draw.rect(screen, yellow, (self.x - 55, self.y + 60, 100 * gratio, 10))

    def gendraw(self):
        self.draw()
        self.drawbar()

    def set(self, i):
        k = int(i % 3)
        i = int(i / 3)
        self.x = 680 + i * 120
        self.y = 560 + k * 120
        self.rect.center = (self.x, self.y)

    def eset(self, i):
        k = int(i % 3)
        i = int(i / 3)
        self.x = 680 + i * 120
        self.y = 60 + k * 120
        self.rect.center = (self.x, self.y)

# UI contents
def draw_scroll(num):
    ratio = num / 500
    pygame.draw.rect(screen, gray, (50, 100, 200, 10))
    pygame.draw.rect(screen, yellow, (50, 100, 200 * ratio, 10))

def draw_time(num):
    ratio = num / 200
    pygame.draw.rect(screen, gray, (50, 100, 200, 10))
    pygame.draw.rect(screen, green, (50, 100, 200 * ratio, 10))

def drawgrid():
    for i in range(3):
        for k in range(3):
            pygame.draw.rect(screen, white, (600 + k * 130, 500 + i * 130, 130, 130))

# unit contents
def tank():
    tank = Ship(0, 0, 'etank', 50, 10, 'tank', 120, 200)
    return tank

def tankadd(list, i):
    list[i] = tank()
    list[i].set(i)

def dps():
    dps = Ship(0, 0, 'edps', 30, 15)

def pick():
    for event in pygame.event.get():
        while event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # print(pos)
            if (pos[0] > 600 & pos[0] < 990):
                if (pos[1] > 500 & pos[1] < 890):
                    i = int((pos[0] - 600) / 130) + int((pos[0] - 600) % 130 > 0) - 1
                    k = int((pos[1] - 500) / 130) + int((pos[1] - 500) % 130 > 0) - 1
                    # print(i*3+k)
                    return (i * 3 + k)
                print("please choose inside the grid")
            print("please choose inside the grid")


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    global money

    # boot speed
    bootspeed = 1
    time_scroll = 0
    # screen set up
    mothership = Ship(800, 680, 'Mothership', 300, 10, 'player', 0, 100)
    enemy1 = Ship(680, 180, 'etank', 50, 10, 'tank', 120, 200)
    enemy4 = Ship(800, 180, 'eMothership', 200, 10, 'player', 0, 100)
    enemy3 = Ship(800, 300, 'etank', 50, 10, 'tank', 120, 200)
    enemylist[1] = enemy1
    enemylist[4] = enemy4

    time = 0
    tick = 1
    timespeed = 1
    run = True
    tig = 1
    while run:
        clock.tick(fps)
        # Clear the screen
        screen.fill(black)
        # Draw UI components
        draw_bg()
        draw_grid()
        draw_money()
        draw_scroll(time_scroll)
        draw_panel()
        draw_radar()
        draw_ship_icons()

        if tig == 1:
            for enemy in enemylist:
                if enemy is not None:
                    enemy.gendraw()

            shipos = pick()
            next_ship, next_ship_index = get_next_ship(current_ship_index)
            draw_next_ship(screen, next_ship)
            if shipos:
                mothership.set(shipos)
                mylist[shipos] = mothership
                tig = 2

        if tig == 2:
            bootspeed = 1
            time_scroll += bootspeed

        for ship in mylist:
            if ship is not None:
                ship.gendraw()

        for enemy in enemylist:
            if enemy is not None:
                enemy.gendraw()

        for count, myship in enumerate(mylist):
            if myship is not None:
                if myship.alive:
                    if myship.gauge < myship.max_gauge:
                        myship.gauge += bootspeed
                if myship.gauge == myship.max_gauge:
                    myship.attack()
                    myship.gauge = 0

                if enemy4.alive == False:
                    bootspeed = 0

        if tig == 2:
            for count, enemy in enumerate(enemylist):
                if enemy is not None:
                    if enemy.alive == True:
                        if enemy.gauge < enemy.max_gauge:
                            enemy.gauge += bootspeed
                        if enemy.gauge == enemy.max_gauge:
                            enemy.attack()
                            enemy.gauge = 0
                        if mothership.alive == False:
                            print("You lose")
                            bootspeed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tig == 1:
                    # Handle ship selection
                    ship_selection_y = 350
                    for ship_name in ship_images.keys():
                        if 10 <= event.pos[0] <= 110 and ship_selection_y <= event.pos[1] <= ship_selection_y + 100:
                            if money >= ship_prices[ship_name]:
                                next_ship = ship_name
                                mothership = Ship(800, 680, next_ship, 300, 10, 'player', 0, 100)
                                money -= ship_prices[next_ship]
                                tig = 2
                                break
                        ship_selection_y += 140

        if time_scroll >= 500:
            tig = 3
            for b in range(9):
                if mylist[b] is not None:
                    if mylist[b].alive != True:
                        mylist[b] = None

            for v in range(9):
                if enemylist[v] is not None:
                    if enemylist[v].alive != True:
                        enemylist[v] = None

            bootspeed = 0
            time += timespeed
            if tick == 1:
                tankadd(mylist, 2)
                tankadd(mylist, 3)
            draw_time(time)

            if time == 200:
                tick += 1
                print("tick is :")
                print(tick)
                money += 100
                time_scroll = 0
                bootspeed = 1
                time = 0
                tig = 2

        # Update the display
        pygame.display.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()