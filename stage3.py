import pygame
from constant import black, green, blue, gray, yellow, bottom_panel, screen_width, screen_height, white
import random

IMG_PATH = "/Users/kesleyrana/Documents/VSCode/CMPT276/Quetzal_CMPT276/Phase3/img/"
#
mode = random.randint(0, 1)
print("our ai mode this time is:")
print(mode)

# next stage: buying, setting UI and dataclass preparing

# ... (all the imports and constants)
screen = pygame.display.set_mode((screen_width, screen_height))
panel = pygame.image.load(IMG_PATH + 'panel.png').convert_alpha()
sgrid = pygame.image.load(IMG_PATH + '3x3.png').convert_alpha()
egrid = pygame.image.load(IMG_PATH + '3x3.png').convert_alpha()
radar = pygame.image.load(IMG_PATH + 'radar.png').convert_alpha()
exp = pygame.image.load(IMG_PATH + 'exp.png').convert_alpha()
fire = pygame.image.load(IMG_PATH + 'fire.png').convert_alpha()
background_img = pygame.image.load(IMG_PATH + 'sea.png').convert_alpha()

# Board set up
enemylist = [None] * 9
mylist = [None] * 9
money = 200
emoney = 100
tinventory = 0
einventory = 0
set = 'tank'

ship_img = ["etank", "Mothership"]  # Update the names as needed
ship_prices = {"etank": 100}
ship_images = {ship: pygame.image.load(f'/Users/kesleyrana/Documents/VSCode/CMPT276/Quetzal_CMPT276/Phase3/img/{ship}/0.png').convert_alpha() for ship in ship_img}


def setdisplay():
    font = pygame.font.SysFont(None, 24)
    text = font.render(f'Now you can deploy {set}', True, (255, 255, 255))
    text2 = font.render('click E to change what you want to deploy', True, (255, 255, 255))
    screen.blit(text, (10, 200))
    screen.blit(text2, (40, 224))


def drawinven():
    font = pygame.font.SysFont(None, 24)
    global tinventory
    global einventory
    x = tinventory
    z = einventory
    text = font.render(f'Tank inventory: {x}', True, (255, 255, 255))
    text2 = font.render(f'DPS inventory: {z}', True, (255, 255, 255))
    screen.blit(text, (40, 454))
    screen.blit(text2, (40, 554))


# Define current ship index
current_ship_index = 0


def get_next_ship(current_index):
    next_index = (current_index + 1) % len(ship_img)
    return ship_img[next_index], next_index


def draw_next_ship(screen, ship_name):
    font = pygame.font.SysFont(None, 30)
    text = font.render(f'Place mothership on the board', True, (255, 255, 255))
    screen.blit(text, (screen_width - 300, 10))
    screen.blit(ship_images[ship_name], (screen_width - 285, 20))


# buy ui
def draw_ship_icons():
    y = 350
    img = pygame.image.load(IMG_PATH + 'shop/tankbuy.png').convert_alpha()
    screen.blit(img, (10, y))
    font = pygame.font.SysFont(None, 24)
    price_text = font.render(f'Price: $100', True, (255, 255, 255))
    screen.blit(price_text, (40, y + 80))

    dpsimg = pygame.image.load(IMG_PATH + 'shop/tankbuy.png').convert_alpha()
    screen.blit(dpsimg, (10, y + 120))
    font = pygame.font.SysFont(None, 24)
    dpsprice_text = font.render(f'Price: $100', True, (255, 255, 255))
    screen.blit(dpsprice_text, (40, y + 180))


# winlose
def drawwin(screen):
    font = pygame.font.SysFont(None, 44)
    text = font.render('Victory!', True, (255, 255, 255))
    screen.blit(text, (screen_width - 280, 10))


def drawlose(screen):
    font = pygame.font.SysFont(None, 30)
    text = font.render('Defeated! Lets try again', True, (255, 255, 255))
    screen.blit(text, (screen_width - 280, 10))


def draw_info(screen):
    font = pygame.font.SysFont(None, 24)
    text = font.render('Take down enemy mothership!', True, (255, 255, 255))
    atext = font.render('Buy and deploy dps ship', True, (255, 255, 255))
    screen.blit(text, (screen_width - 280, 10))
    screen.blit(atext, (screen_width - 280, 34))


def draw_money():
    money_info = f'CURRENT MONEY: $ {money}'
    myFont = pygame.font.SysFont("Times New Roman", 32)
    moneyDisplay = myFont.render(str(money_info), 1, black)
    screen.blit(moneyDisplay, (30, 30))
    emoney_info = f'Enemy MONEY: $ {emoney}'
    emoneyDisplay = myFont.render(str(emoney_info), 1, black)
    screen.blit(emoneyDisplay, (30, 62))


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
        img = pygame.image.load(f'/Users/kesleyrana/Documents/VSCode/CMPT276/Quetzal_CMPT276/Phase3/img/{self.name}/Idel/{0}.png')
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
            if self.type == 'tank' or 'player' or 'dps':
                for z in range(3):

                    if enemylist[z + i * 3] is not None:
                        if enemylist[z + i * 3].hp > 0:
                            a = z + i * 3
                            # print("e samerow attack")
                            # print(a)
                            break
                if a == 0:
                    z = 0
                    # print(z)
                    for z in range(9):
                        # print(z)
                        if enemylist[z] is not None:
                            # print(z)
                            if enemylist[z].hp > 0:
                                a = z
                                # print("e different row attack")
                                # print(a)
                                break
        if k == 2:
            if self.type == 'tank' or 'player' or 'dps':
                for z in range(3):
                    if mylist[z + i * 3] is not None:
                        if mylist[z + i * 3].hp > 0:
                            a = z + i * 3
                            # print("samerow attack")
                            # print(a)
                            break
                if a == 0:
                    for z in range(9):
                        if mylist[z] is not None:
                            if mylist[z].hp > 0:
                                a = z
                                # print("diffrent  row attack")
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
                    # if enemylist[a].type != 'aMothership':
                    #    print("+money")
                    #    global money
                    #    money += 50
                    #    print(money)
                draw_exp(enemylist[a].x, enemylist[a].y)

        if k == 2:
            # print("mylist index")
            # print(a)
            if mylist[a] is not None:
                mylist[a].hp -= damage
                if mylist[a].hp <= 0:
                    mylist[a].alive = False
                    # print(a)
                    print("our ship lost")
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
        self.y = 300 - k * 120
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


# unit contents
def tank():
    tank = Ship(0, 0, 'etank', 100, 8, 'tank', 240, 400)
    return tank


def tankadd(list, i):
    list[i] = tank()
    list[i].set(i)
    i = None


def etankadd(list, i):
    list[i] = tank()
    list[i].eset(i)


def dps():
    dps = Ship(0, 0, 'edps', 50, 25, 'dps', 0, 150)
    return dps


def dpsadd(list, i):
    list[i] = dps()
    list[i].set(i)


def edpsadd(list, i):
    list[i] = dps()
    list[i].eset(i)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    global money
    global set
    global tinventory
    global einventory
    global emoney
    # boot speed
    bootspeed = 0
    time_scroll = 0
    # screen set up
    mothership = Ship(0, 0, 'Mothership', 500, 20, 'player', 0, 200)

    enemy4 = Ship(800, 60, 'eMothership', 500, 20, 'player', 0, 200)
    enemy4.eset(7)

    edpsadd(enemylist, 8)
    enemylist[7] = enemy4

    d = None
    time = 0
    tick = 1
    timespeed = 1
    run = True
    tig = 1
    shipos = None
    while run:
        bootspeed = 0
        clock.tick(fps)
        draw_bg()
        # drawgrid()
        draw_grid()
        draw_money()
        draw_scroll(time_scroll)
        draw_panel()
        draw_radar()
        draw_ship_icons()
        drawinven()
        setdisplay()
        if tig == 1:
            for enemy in enemylist:
                if enemy is not None:
                    enemy.gendraw()

            next_ship, lop = get_next_ship(current_ship_index)
            draw_next_ship(screen, next_ship)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if (pos[0] > 600 & pos[0] < 990):
                        if (pos[1] > 500 & pos[1] < 890):
                            i = int((pos[0] - 600) / 130) + int((pos[0] - 600) % 130 > 0) - 1
                            k = int((pos[1] - 500) / 130) + int((pos[1] - 500) % 130 > 0) - 1

                            shipos = i * 3 + k
                            # print(shipos)
                            # print(shipos)
                            if shipos in range(9):
                                mothership.set(shipos)
                                mylist[shipos] = mothership
                                tig = 2
                                shipos = None

        if tig == 2:
            bootspeed = 1
            time_scroll += bootspeed
            draw_info(screen)

        for ship in mylist:
            if ship is not None:
                ship.gendraw()

        for enemy in enemylist:
            if enemy is not None:
                enemy.gendraw()

        if enemy4.hp <= 200:
            if emoney >= 100:
                if enemylist[6] == None:
                    etankadd(enemylist, 6)
                    emoney -= 100
        if mode == 1:
            if emoney >= 200:

                if enemylist[4] != None:
                    if enemylist[4].hp <= 25:
                        if emoney >= 100:
                            etankadd(enemylist, 3)
                            print('type1')
                        emoney -= 100
                if enemylist[4] == None:
                    if emoney >= 100:
                        etankadd(enemylist, 4)
                        print('type4')
                        emoney -= 100
                if enemylist[5] == None:
                    if emoney >= 100:
                        edpsadd(enemylist, 5)
                        emoney -= 100

                if enemylist[1] == None:
                    if emoney >= 100:
                        etankadd(enemylist, 1)
                        print('type1')
                        emoney -= 100

                if enemylist[2] == None:
                    if emoney >= 100:
                        edpsadd(enemylist, 2)
                        emoney -= 100

        if mode == 0:
            if emoney >= 300:

                if enemylist[3] == None:
                    if emoney >= 100:
                        etankadd(enemylist, 3)
                        emoney -= 100
                if enemylist[4] == None:
                    if emoney >= 100:
                        edpsadd(enemylist, 4)
                        emoney -= 100
                if enemylist[5] == None:
                    if emoney >= 100:
                        edpsadd(enemylist, 5)
                        emoney -= 100

                if enemylist[1] == None:
                    if emoney >= 100:
                        etankadd(enemylist, 1)
                        emoney -= 100

                if enemylist[2] == None:
                    if emoney >= 100:
                        edpsadd(enemylist, 2)
                        emoney -= 100

        if tig == 2:
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
                        tig = 4
                        print("You win")

        if bootspeed == 0:
            if enemy4.hp <= 0:
                drawwin(screen)
            if mothership.alive == False:
                drawlose(screen)

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
                            tig = 4

                            # run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                k = pygame.key.name(event.key)

                if k == 'e':
                    print('changed')
                    if set == 'tank':
                        set = 'dps'
                    else:
                        set = 'tank'

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] in range(10, 110) and pos[1] in range(350, 430):
                    if money >= 100:
                        money -= 100
                        tinventory += 1
                elif pos[0] in range(10, 110) and pos[1] in range(435, 545):
                    if money >= 100:
                        money -= 100
                        einventory += 1

                if (set == 'tank'):
                    if tinventory > 0:
                        # print("ready to print")
                        pos = pygame.mouse.get_pos()
                        if (pos[0] > 600 & pos[0] < 990):
                            if (pos[1] > 500 & pos[1] < 890):
                                i = int((pos[0] - 600) / 130) + int((pos[0] - 600) % 130 > 0) - 1
                                k = int((pos[1] - 500) / 130) + int((pos[1] - 500) % 130 > 0) - 1
                                # print(i*3+k)
                                if i * 3 + k in range(9):
                                    if mylist[i * 3 + k] == None:
                                        d = i * 3 + k

                                    if (d):
                                        if mylist[d] == None:
                                            # print(d)
                                            tankadd(mylist, d)
                                            tinventory -= 1
                                        d = None
                elif (set == 'dps'):
                    if einventory > 0:
                        # print("ready to print")
                        pos = pygame.mouse.get_pos()
                        if (pos[0] > 600 & pos[0] < 990):
                            if (pos[1] > 500 & pos[1] < 890):
                                i = int((pos[0] - 600) / 130) + int((pos[0] - 600) % 130 > 0) - 1
                                k = int((pos[1] - 500) / 130) + int((pos[1] - 500) % 130 > 0) - 1
                                # print(i*3+k)
                                if i * 3 + k in range(9):
                                    if mylist[i * 3 + k] == None:
                                        d = i * 3 + k

                                    if (d):
                                        if mylist[d] == None:
                                            # print(d)
                                            dpsadd(mylist, d)
                                            einventory -= 1
                                        d = None
        if time_scroll >= 500:
            tig = 3
            # if event.type == pygame.MOUSEBUTTONDOWN:

            for b in range(9):
                if mylist[b] is not None:
                    if mylist[b].alive != True:
                        mylist[b] = None

            for v in range(9):
                if enemylist[v] is not None:
                    if enemylist[v].alive != True:
                        enemylist[v] = None

            if time == 10:
                money = int(money * 1.2)
                emoney = int(emoney * 1.2)
                emoney += 100
                money += 100

            bootspeed = 0
            time += timespeed

            draw_time(time)
            # if tick ==2:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (set == 'tank'):
                    if tinventory > 0:
                        # print("ready to print")
                        pos = pygame.mouse.get_pos()
                        if (pos[0] > 600 & pos[0] < 990):
                            if (pos[1] > 500 & pos[1] < 890):
                                i = int((pos[0] - 600) / 130) + int((pos[0] - 600) % 130 > 0) - 1
                                k = int((pos[1] - 500) / 130) + int((pos[1] - 500) % 130 > 0) - 1
                                # print(i*3+k)
                                if i * 3 + k in range(9):
                                    if mylist[i * 3 + k] == None:
                                        d = i * 3 + k

                                    if (d):
                                        if mylist[d] == None:
                                            # print(d)
                                            tankadd(mylist, d)
                                            tinventory -= 1
                                        d = None
                elif (set == 'dps'):
                    if einventory > 0:
                        # print("ready to print")
                        pos = pygame.mouse.get_pos()
                        if (pos[0] > 600 & pos[0] < 990):
                            if (pos[1] > 500 & pos[1] < 890):
                                i = int((pos[0] - 600) / 130) + int((pos[0] - 600) % 130 > 0) - 1
                                k = int((pos[1] - 500) / 130) + int((pos[1] - 500) % 130 > 0) - 1
                                # print(i*3+k)
                                if i * 3 + k in range(9):
                                    if mylist[i * 3 + k] == None:
                                        d = i * 3 + k

                                    if (d):
                                        if mylist[d] == None:
                                            # print(d)
                                            dpsadd(mylist, d)
                                            einventory -= 1
                                        d = None
            if time == 200:
                tick += 1
                print("tick is :")
                print(tick)

                time_scroll = 0
                bootspeed = 1
                time = 0
                tig = 2
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()