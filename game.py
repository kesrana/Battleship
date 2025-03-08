import pygame
import sys
from pygame.locals import *
from button import Button
import random

import stage1, stage2, stage3
from constant import screen_width, screen_height

pygame.init()

SCREEN_SIZE = (1272, 847)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LBLUE = (0, 0, 200)
RED = (255, 0, 0)
MARK = (10, 10, 10)

DEFAULT_FONT_SIZE = 75

GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_SIZE = 50

ASSET_PATH = "/Users/kesleyrana/Documents/VSCode/CMPT276/Quetzal_CMPT276/Phase3/assets/"

# hard code to let mouse click
mouse_pos = (720, 200)  # mouse click position
mouse_button = 1  # 1 is left key on mouse
mouse_event = pygame.event.Event(MOUSEBUTTONDOWN,
                                 button=mouse_button,
                                 pos=mouse_pos)


class GameState:
    MAIN_MENU = 0
    PLAYING = 1
    OPTIONS = 2
    QUIT = 3
    SWITCHER = 4
    STAGE = 5


class ShipPiece:

    def __init__(self, x, y, image_path, scale=1.0):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dragging = False
        self.offset = (self.rect.width * scale / 2, self.rect.height * scale / 2)
        self.scale_image(scale)

    def scale_image(self, scale):
        width = int(self.rect.width * scale)
        height = int(self.rect.height * scale)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.x = roundNum(mouse_pos[0]) - self.offset[0]
            grid_offset = 17.5
            self.rect.y = roundNum(mouse_pos[1], grid_offset) - self.offset[1]

    def render(self, screen):
        screen.blit(self.image, self.rect)


class Game:

    def __init__(self):
        self.player_game_board = None
        self.opponent_game_board = None
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Battleship")
        self.clock = pygame.time.Clock()
        self.state = GameState.MAIN_MENU
        self.buttons = []
        self.game_board = []
        self.rounds = 0
        self.player_turn = True
        self.player_board_clicked = False
        self.opponent_board_clicked = False
        self.clicked_cells = set()
        self.ships_confirmed = False
        self.show_confirm_button = True
        self.ship_pieces = [
            ShipPiece(500, 150, ASSET_PATH + "Ship.png", 2.0),
            ShipPiece(500, 300, ASSET_PATH + "Ship.png", 2.0),
            ShipPiece(500, 450, ASSET_PATH + "Ship.png", 2.0),
            ShipPiece(500, 600, ASSET_PATH + "Ship.png", 2.0),
            ShipPiece(500, 750, ASSET_PATH + "Ship.png", 2.0)
        ]
        self.playerpiece = 0
        self.enemypiece = 0
        self.checkcon = 0
        self.moves_log = []
        self.state_last = GameState.MAIN_MENU
        self.volume_on = True
        self.volume_level = 50
        self.starting = True
        self.difficulty = 2

    def render_grid_lines(self, position, grid_width, grid_height, cell_size):
        x, y = position

        # Draw vertical grid lines
        for i in range(grid_width + 1):
            start_pos = (x + i * cell_size, y)
            end_pos = (x + i * cell_size, y + grid_height * cell_size)
            pygame.draw.line(self.screen, BLACK, start_pos, end_pos)

        # Draw horizontal grid lines
        for i in range(grid_height + 1):
            start_pos = (x, y + i * cell_size)
            end_pos = (x + grid_width * cell_size, y + i * cell_size)
            pygame.draw.line(self.screen, BLACK, start_pos, end_pos)

    def checkwin(self):
        if self.playerpiece == 0:
            self.update()
            self.render()
            pygame.time.delay(1000)
            self.checkcon = 1
            self.aiwin()
        elif self.enemypiece == 0:
            self.update()
            self.render()
            pygame.time.delay(1000)
            self.checkcon = 1
            self.playwin()

    def get_difficulty_name(self):
        if self.difficulty == 1:
            return "Easy"
        elif self.difficulty == 2:
            return "Medium"
        elif self.difficulty == 3:
            return "Hard"

    def playwin(self):
        bg_image = pygame.image.load(ASSET_PATH + "4.png")
        self.screen.blit(bg_image, (0, 0))  # Use the game board background as the screen background

        win_text = get_font(32).render("YOU WIN!", True, "Black")
        self.screen.blit(win_text, (50, 50))
        pygame.display.flip()

        print("Player wins")
        pygame.time.delay(4000)
        self.state = GameState.MAIN_MENU

    def aiwin(self):
        bg_image = pygame.image.load(ASSET_PATH + "4.png")
        self.screen.blit(bg_image, (0, 0))  # Use the game board background as the screen background

        lose_text = get_font(32).render("AI WINS!", True, "Black")
        self.screen.blit(lose_text, (50, 50))
        pygame.display.flip()

        print("AI wins")
        pygame.time.delay(4000)
        self.state = GameState.MAIN_MENU

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.OPTIONS
            if self.state == GameState.MAIN_MENU:
                self.state_last = GameState.MAIN_MENU
                self.handle_main_menu_events(event)
            elif self.state == GameState.PLAYING:
                self.state_last = GameState.PLAYING
                self.handle_playing_events(event)
            elif self.state == GameState.OPTIONS:
                self.handle_options_events(event)
            elif self.state == GameState.SWITCHER:
                self.handle_switcher_events(event)
            elif self.state == GameState.STAGE:
                self.handle_stage_events(event)

    def update(self):
        if self.state == GameState.MAIN_MENU:
            self.update_main_menu()
        elif self.state == GameState.PLAYING:
            self.update_playing()
        elif self.state == GameState.OPTIONS:
            self.update_options()
        elif self.state == GameState.SWITCHER:
            self.update_switcher()
        elif self.state == GameState.STAGE:
            self.update_stage()

    def render(self):
        self.screen.fill(WHITE)
        if self.state == GameState.MAIN_MENU:
            self.render_main_menu()
        elif self.state == GameState.PLAYING:
            self.render_playing()
        elif self.state == GameState.OPTIONS:
            self.render_options()
        elif self.state == GameState.SWITCHER:
            self.render_switcher()
        elif self.state == GameState.STAGE:
            self.render_stage()
        pygame.display.update()

    def handle_main_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.checkForInput(mouse_pos):
                    if button.text_input == "PLAY":
                        self.state = GameState.SWITCHER
                        self.show_confirm_button = True
                        # Reset relevant game variables
                        self.starting = True
                        self.ships_confirmed = False
                        self.clicked_cells = set()
                        self.rounds = 0
                        self.player_turn = True
                        self.player_board_clicked = False
                        self.opponent_board_clicked = False
                    elif button.text_input == "OPTIONS":
                        self.state = GameState.OPTIONS
                    elif button.text_input == "QUIT":
                        pygame.quit()
                        sys.exit()

    def update_main_menu(self):
        self.buttons = [
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(640, 250),
                   text_input="PLAY",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="#d7fcd4",
                   hovering_color="White"),
            Button(image=pygame.image.load(ASSET_PATH + "Options Rect.png"),
                   pos=(640, 400),
                   text_input="OPTIONS",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="#d7fcd4",
                   hovering_color="White"),
            Button(image=pygame.image.load(ASSET_PATH + "Quit Rect.png"),
                   pos=(640, 550),
                   text_input="QUIT",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="#d7fcd4",
                   hovering_color="White")
        ]

    def render_main_menu(self):
        bg_image = pygame.image.load(ASSET_PATH + "Background.png")
        self.screen.blit(bg_image, (0, 0))
        menu_text = get_font(100).render("Battleship", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))
        self.screen.blit(menu_text, menu_rect)
        for button in self.buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.screen)

    def log_move(self, move):
        self.moves_log.append(move)
        if len(self.moves_log) > 10:
            self.moves_log.pop(0)

    def handle_playing_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_buttons(event) == False:
                if self.starting == True:
                    self.handle_dragging_ships(event)
                else:
                    self.handle_gameplay(event)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                for ship in self.ship_pieces:
                    ship.dragging = False

    def handle_buttons(self, event):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.checkForInput(mouse_pos):
                if button.text_input == "Return":
                    self.state = GameState.MAIN_MENU
                    return True
                elif button.text_input == "Confirm Ships":
                    valid_ships = True
                    xBoundary = (50, 350)
                    yBoundary = (133, 583)
                    xDistance = 175
                    for ship in self.ship_pieces:
                        if ship.rect.x < xBoundary[0] or ship.rect.x > xBoundary[
                            1] or ship.rect.y < yBoundary[0] or ship.rect.y > yBoundary[1]:
                            valid_ships = False
                        for ship2 in self.ship_pieces:
                            if ship != ship2 and ship.rect.y == ship2.rect.y and abs(
                                    ship.rect.x - ship2.rect.x) < xDistance:
                                valid_ships = False
                                break
                    if valid_ships:
                        self.starting = False
                        self.ships_confirmed = True
                        array = []
                        for ship in self.ship_pieces:
                            coord = (ship.rect.x, ship.rect.y)
                            array.append(coord)
                        self.place_ships(array)
                        self.buttons.remove(button)
                        self.show_confirm_button = False
                    return True
        return False

    def handle_dragging_ships(self, event):
        mouse_pos = pygame.mouse.get_pos()
        xDistance = 100
        yDistance = 25
        for ship in self.ship_pieces:
            if abs(mouse_pos[0] - ship.rect.x -
                   ship.offset[0]) < xDistance and abs(mouse_pos[1] - ship.rect.y -
                                                       ship.offset[1]) < yDistance:
                if event.button == pygame.BUTTON_LEFT:
                    temp = False
                    for ship2 in self.ship_pieces:
                        if ship2.dragging == True and ship2 != ship:
                            temp = True
                    if temp == False:
                        ship.dragging = True

    def handle_gameplay(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.player_turn:
            if not self.player_board_clicked:
                for row in self.opponent_game_board:
                    for cell in row:
                        if cell.rect.collidepoint(mouse_pos):
                            if cell in self.clicked_cells:
                                self.player_board_clicked = False
                                break
                            if not cell.is_hit and not cell.is_miss:
                                self.player_board_clicked = True
                                self.clicked_cells.add(cell)
                                if cell.is_ship:
                                    cell.color = RED
                                    self.enemypiece -= 1
                                    self.rounds += 1
                                    self.log_move("Player hit at ({}, {})".format(
                                        cell.rect.x, cell.rect.y))
                                    self.checkwin()
                                    self.player_board_clicked = False
                                else:
                                    cell.color = LBLUE
                                    self.rounds += 1
                                    self.log_move("Player missed at ({}, {})".format(
                                        cell.rect.x, cell.rect.y))
                                    self.player_turn = False
                                break
                if self.player_board_clicked:
                    self.opponent_board_clicked = False
                    pygame.event.post(mouse_event)
            else:
                pass
        else:
            if not self.opponent_board_clicked:
                if self.player_board_clicked:
                    if self.difficulty == 3:
                        self.hard_ai()
                    elif self.difficulty == 2:
                        self.medium_ai()
                    else:
                        self.easy_ai()
            if self.opponent_board_clicked:
                self.player_board_clicked = False

    def easy_ai(self):
        available_cells = []
        for row in self.player_game_board:
            for cell in row:
                if not cell.is_hit and not cell.is_miss:
                    available_cells.append(cell)
        if available_cells:
            cell_to_hit = random.choice(available_cells)
            self.opponent_shoot_check(cell_to_hit)

    def medium_ai(self):
        for row, row_value in enumerate(self.player_game_board):
            for cell, cell_value in enumerate(row_value):
                if cell_value.is_hit:
                    if row + 1 < len(self.player_game_board) and row - 1 >= 0:
                        if self.player_game_board[row + 1][cell].is_hit:
                            if not (self.player_game_board[row - 1][cell].is_hit
                                    or self.player_game_board[row - 1][cell].is_miss):
                                cell_to_hit = self.player_game_board[row - 1][cell]
                                self.opponent_shoot_check(cell_to_hit)
                                return
                        if self.player_game_board[row - 1][cell].is_hit:
                            if not (self.player_game_board[row + 1][cell].is_hit
                                    or self.player_game_board[row + 1][cell].is_miss):
                                cell_to_hit = self.player_game_board[row + 1][cell]
                                self.opponent_shoot_check(cell_to_hit)
                                return
                    if cell + 1 < len(row_value) and cell - 1 >= 0:
                        if self.player_game_board[row][cell + 1].is_hit:
                            if not (self.player_game_board[row][cell - 1].is_hit
                                    or self.player_game_board[row][cell - 1].is_miss):
                                cell_to_hit = self.player_game_board[row][cell - 1]
                                self.opponent_shoot_check(cell_to_hit)
                                return
                        if self.player_game_board[row][cell - 1].is_hit:
                            if not (self.player_game_board[row][cell + 1].is_hit
                                    or self.player_game_board[row][cell + 1].is_miss):
                                cell_to_hit = self.player_game_board[row][cell + 1]
                                self.opponent_shoot_check(cell_to_hit)
                                return
        for row, row_value in enumerate(self.player_game_board):
            for cell, cell_value in enumerate(row_value):
                if cell_value.is_hit:
                    if row + 1 < len(self.player_game_board) and self.player_game_board[
                        row + 1][cell].is_hit:
                        continue
                    if row - 1 >= 0 and self.player_game_board[row - 1][cell].is_hit:
                        continue
                    if cell + 1 < len(row_value) and self.player_game_board[row][
                        cell + 1].is_hit:
                        continue
                    if cell - 1 >= 0 and self.player_game_board[row][cell - 1].is_hit:
                        continue
                    i = random.randint(0, 3)
                    for j in range(4):
                        if int(i / 2) == 0:
                            if cell + (i * 2 - 1) >= 0 and cell + (i * 2 -
                                                                   1) < len(row_value):
                                if not (self.player_game_board[row][cell + (i * 2 - 1)].is_hit
                                        or self.player_game_board[row][cell +
                                                                       (i * 2 - 1)].is_miss):
                                    cell_to_hit = self.player_game_board[row][cell + (i * 2 - 1)]
                                    self.opponent_shoot_check(cell_to_hit)
                                    return
                        else:
                            if row + ((i % 2) * 2 - 1) >= 0 and row + (
                                    (i % 2) * 2 - 1) < len(self.player_game_board):
                                if not (self.player_game_board[row +
                                                               ((i % 2) * 2 - 1)][cell].is_hit
                                        or self.player_game_board[row + (
                                                (i % 2) * 2 - 1)][cell].is_miss):
                                    cell_to_hit = self.player_game_board[row +
                                                                         ((i % 2) * 2 - 1)][cell]
                                    self.opponent_shoot_check(cell_to_hit)
                                    return
                        i += 1
                        if i > 3:
                            i = 0

        self.easy_ai()

    def hard_ai(self):
        available_cells = []
        for row in self.player_game_board:
            for cell in row:
                if not cell.is_hit and not cell.is_miss and cell.is_ship:
                    available_cells.append(cell)
        if available_cells:
            cell_to_hit = random.choice(available_cells)
            self.opponent_shoot_check(cell_to_hit)
            return cell_to_hit
        return

    def opponent_shoot_check(self, cell_to_hit):
        if cell_to_hit.is_ship == True:
            cell_to_hit.color = RED
            cell_to_hit.is_hit = True
            self.playerpiece -= 1
            self.log_move("Opponent hit at ({}, {})".format(cell_to_hit.rect.x,
                                                            cell_to_hit.rect.y))
            self.checkwin()
            pygame.time.delay(300)
            pygame.event.post(mouse_event)
        else:
            cell_to_hit.color = BLUE
            cell_to_hit.is_miss = True
            self.log_move("Opponent missed at ({}, {})".format(
                cell_to_hit.rect.x, cell_to_hit.rect.y))
            self.opponent_board_clicked = True
            self.player_turn = True
        return

    def update_playing(self):
        self.buttons = [
            Button(image=pygame.image.load(ASSET_PATH + "Quit Rect.png"),
                   pos=(1100, 50),
                   text_input="Return",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="#d7fcd4",
                   hovering_color="White")
        ]
        if not self.ships_confirmed:
            self.buttons.append(
                Button(image=pygame.transform.scale(
                    pygame.image.load(ASSET_PATH + "Quit Rect.png"), (400, 70)),
                    pos=(975, 750),
                    text_input="Confirm Ships",
                    font=get_font(50),
                    base_color="#d7fcd4",
                    hovering_color="White"))
        if self.state == GameState.MAIN_MENU:
            for ship in self.ship_pieces:
                ship.rect.x = 500
                ship.rect.y = 150 + self.ship_pieces.index(ship) * 150
                ship.dragging = False
            self.player_turn = True
            self.starting = True
            self.ships_confirmed = False
            self.clicked_cells = set()
            self.rounds = 0
            self.player_board_clicked = False
            self.opponent_board_clicked = False

        if self.checkcon == 0:
            for row in self.player_game_board:
                for cell in row:
                    cell.update()

            for row in self.opponent_game_board:
                for cell in row:
                    cell.update()

        for ship in self.ship_pieces:
            if ship.dragging:
                mouse_pos = pygame.mouse.get_pos()
                ship.rect.x = roundNum(mouse_pos[0]) - ship.offset[0]
                grid_offset = 17.5
                ship.rect.y = roundNum(mouse_pos[1], grid_offset) - ship.offset[1]
            ship.update()

    def render_playing(self):
        bg_image = pygame.image.load(ASSET_PATH + "4.png")
        self.screen.blit(bg_image, (0, 0))

        esc_text = get_font(32).render("Press Esc to Open Settings", True, 'Black')
        self.screen.blit(esc_text, (20, 20))
        i1_text = get_font(32).render("PlayerBoard", True, "Black")
        i2_text = get_font(32).render("EnemyBoard", True, "Black")
        self.screen.blit(i1_text, (200, 150))
        self.screen.blit(i2_text, (870, 150))

        for row in self.player_game_board:
            for cell in row:
                cell.render(self.screen)
        self.render_grid_lines((50, 200), GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)

        for row in self.opponent_game_board:
            for cell in row:
                cell.render(self.screen)
        self.render_grid_lines((720, 200), GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)

        for button in self.buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.screen)

        if self.ships_confirmed:
            for button in self.buttons:
                if button.text_input == "Confirm Ships":
                    continue

        if self.show_confirm_button:
            for button in self.buttons:
                if button.text_input == "Confirm Ships":
                    button.changeColor(pygame.mouse.get_pos())
                    button.update(self.screen)

        if self.player_turn:
            if self.starting == True:
                turn_text = get_font(32).render(
                    "Place Ship Pieces On The Board And Confirm", True, BLACK)
            elif not self.player_board_clicked:
                turn_text = get_font(32).render(
                    "Player's Turn - Click Opponent's Board", True, BLACK)
            else:
                turn_text = get_font(32).render(
                    "Player's Turn - Waiting for Opponent's Move", True, BLACK)
        else:
            if not self.opponent_board_clicked:
                turn_text = get_font(32).render("Opponent's Turn - Click Your Board",
                                                True, BLACK)
            else:
                turn_text = get_font(32).render(
                    "Opponent's Turn - Waiting for Your Move", True, BLACK)
        turn_rect = turn_text.get_rect(topright=(1250, 800))
        self.screen.blit(turn_text, turn_rect)
        rounds_text = get_font(32).render("Rounds: " + str(self.rounds), True,
                                          BLACK)
        rounds_rect = rounds_text.get_rect(topright=(720, 50))
        self.screen.blit(rounds_text, rounds_rect)

        for ship in self.ship_pieces:
            ship.render(self.screen)

        move_log_text = get_font(24).render("Move Log:", True, BLACK)
        self.screen.blit(move_log_text, (20, 750))

        if len(self.moves_log) >= 2:
            move_text1 = get_font(24).render(self.moves_log[-2], True, BLACK)
            move_text2 = get_font(24).render(self.moves_log[-1], True, BLACK)
            self.screen.blit(move_text1, (20, 780))
            self.screen.blit(move_text2, (20, 810))
        elif len(self.moves_log) == 1:
            move_text1 = get_font(24).render(self.moves_log[-1], True, BLACK)
            self.screen.blit(move_text1, (20, 780))

    def get_last_move(self, player):
        for move in reversed(self.moves_log):
            if move.startswith(player):
                return move
        return ""

    def handle_stage_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.checkForInput(mouse_pos):
                    if button.text_input == "Level 1":
                        pygame.display.set_mode((screen_width, screen_height))
                        stage1.main()
                    if button.text_input == "Level 2":
                        pygame.display.set_mode((screen_width, screen_height))
                        stage2.main()
                    if button.text_input == "Level 3":
                        pygame.display.set_mode((screen_width, screen_height))
                        stage3.main()

    def update_stage(self):
        self.buttons = [
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(180, 260),
                   text_input="Level 1",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="Black",
                   hovering_color="Green"),
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(650, 260),
                   text_input="Level 2",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="Black",
                   hovering_color="Green"),
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(1100, 260),
                   text_input="Level 3",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="Black",
                   hovering_color="Green"),

        ]

    def render_stage(self):
        bg_image = pygame.image.load(ASSET_PATH + "4.png")
        self.screen.blit(bg_image, (0, 0))
        options_text = get_font(DEFAULT_FONT_SIZE).render("Choose game Stage",
                                                          True, "Black")
        options_rect = options_text.get_rect(center=(640, 50))
        self.screen.blit(options_text, options_rect)
        for button in self.buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.screen)

    def handle_switcher_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.checkForInput(mouse_pos):
                    if button.text_input == "Classic":
                        self.state = GameState.PLAYING
                        self.create_game_board()
                    if button.text_input == "New Mode":
                        self.state = GameState.STAGE

    def update_switcher(self):
        self.buttons = [
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(640, 260),
                   text_input="Classic",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="Black",
                   hovering_color="Green"),
            Button(image=pygame.image.load(ASSET_PATH + "Options Rect.png"),
                   pos=(640, 560),
                   text_input="New Mode",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="Black",
                   hovering_color="Green")
        ]

    def render_switcher(self):
        bg_image = pygame.image.load(ASSET_PATH + "4.png")
        self.screen.blit(bg_image, (0, 0))
        options_text = get_font(DEFAULT_FONT_SIZE).render("Choose game model",
                                                          True, "Black")
        options_rect = options_text.get_rect(center=(640, 50))
        self.screen.blit(options_text, options_rect)
        for button in self.buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.screen)

    def handle_options_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.checkForInput(mouse_pos):
                    if button.text_input == "Mute":
                        self.volume_on = not self.volume_on
                        if self.volume_on:
                            self.volume_level = 100
                            pygame.mixer.music.set_volume(1)
                        else:
                            if self.volume_level == 0:
                                self.volume_level = 100
                            pygame.mixer.music.set_volume(0.0)
                        self.update_options()
                    if button.text_input == "BACK":
                        self.state = self.state_last
                        self.state = self.state_last
                    elif "Difficulty" in button.text_input:
                        self.toggle_difficulty()
                    if button.text_input == f"{self.volume_level}%":
                        volume_difference = 25
                        self.volume_level = (self.volume_level - volume_difference)
                        if self.volume_level < 0:
                            self.volume_level = 100
                        pygame.mixer.music.set_volume(self.volume_level / 100.0)

    def toggle_difficulty(self):
        self.difficulty = (self.difficulty % 3) + 1
        self.update_options()

    def update_options(self):
        self.buttons = [
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(640, 560),
                   text_input="BACK",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="Black",
                   hovering_color="Green"),
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(640, 160),
                   text_input="Mute",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="Black",
                   hovering_color="Green"),
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(640, 460),
                   text_input="Difficulty: " + self.get_difficulty_name(),
                   font=get_font(34),
                   base_color="Black",
                   hovering_color="Green"),
            Button(image=pygame.image.load(ASSET_PATH + "Play Rect.png"),
                   pos=(640, 360),
                   text_input=f"{self.volume_level}%" if self.volume_on else "0%",
                   font=get_font(DEFAULT_FONT_SIZE),
                   base_color="Black",
                   hovering_color="Green"),
        ]

    def render_options(self):
        bg_image = pygame.image.load(ASSET_PATH + "4.png")
        self.screen.blit(bg_image, (0, 0))
        options_text = get_font(25).render("ESC to setting menu", True, "Black")
        options_rect = options_text.get_rect(center=(300, 50))
        self.screen.blit(options_text, options_rect)
        options_text1 = get_font(25).render(
            "click 'Back' to continue your game while playing", True, "Black")
        options_rect1 = options_text.get_rect(center=(300, 700))
        self.screen.blit(options_text1, options_rect1)

        for button in self.buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.screen)

    def create_game_board(self):
        self.moves_log = []
        self.starting = True
        ships_per_row = 3
        x_distance = 200
        y_distance = 50
        y_offset = 633
        i = 0
        for ship in self.ship_pieces:
            ship.rect.x = (i % ships_per_row) * x_distance
            ship.rect.y = y_offset + int(i / ships_per_row) * y_distance
            i += 1

        self.player_game_board = []
        for i in range(GRID_HEIGHT):
            row = []
            for j in range(GRID_WIDTH):
                x = j * CELL_SIZE + 50
                y = i * CELL_SIZE + 200
                cell = Cell(x, y, CELL_SIZE, WHITE)
                row.append(cell)
            self.player_game_board.append(row)

        self.create_opponent_board()

        self.buttons.append(
            Button(image=pygame.transform.scale(
                pygame.image.load(ASSET_PATH + "Quit Rect.png"), (400, 70)),
                pos=(975, 750),
                text_input="Confirm Ships",
                font=get_font(50),
                base_color="#d7fcd4",
                hovering_color="White"))

    def create_opponent_board(self):

        random.seed()
        ship_lengths = [4, 4, 4, 4, 4]
        ships = []
        for length in ship_lengths:
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                direction = random.choice(["horizontal", "vertical"])
                points = []

                if direction == "horizontal":
                    if x + length <= GRID_WIDTH:
                        points = [(x + i, y) for i in range(length)]
                elif direction == "vertical":
                    if y + length <= GRID_HEIGHT:
                        points = [(x, y + i) for i in range(length)]

                if points:
                    overlap = False
                    for ship in ships:
                        if any(point in ship for point in points):
                            overlap = True
                            break

                    if not overlap:
                        ships.append(points)
                        break

        self.opponent_game_board = []
        for i in range(GRID_HEIGHT):
            row = []
            for j in range(GRID_WIDTH):
                x = j * CELL_SIZE + 720
                y = i * CELL_SIZE + 200
                cell = Cell(x, y, CELL_SIZE, WHITE)
                for ship in ships:
                    if (j, i) in ship:
                        cell.is_ship = True
                        self.enemypiece += 1
                        break
                row.append(cell)
            self.opponent_game_board.append(row)

    def place_ships(self, coords):
        for coord in coords:
            distance = 50
            x_offset = 50
            y_offset = 133
            x = int((coord[0] - x_offset) / distance)
            y = int((coord[1] - y_offset) / distance)
            for i in range(4):
                self.player_game_board[y][x + i].is_ship = True
        ship_num = 5
        self.playerpiece = 4 * ship_num


class Cell:

    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.is_ship = False
        self.is_hit = False
        self.is_miss = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.is_ship:
                    self.is_hit = True
                else:
                    self.is_miss = True

    def update(self):
        if self.is_hit & self.is_ship:
            self.color = RED
        elif self.is_miss:
            self.color = LBLUE

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


def get_font(size):
    return pygame.font.Font(ASSET_PATH + "font.ttf", size)


def roundNum(num, offset=0):
    grid_length = 50
    if ((num + offset) % grid_length > grid_length / 2):
        num += grid_length - (num + offset) % grid_length
    else:
        num -= (num + offset) % grid_length
    return num


def main():
    pygame.mixer.init()
    pygame.mixer.music.load(ASSET_PATH + 'Battleship.mp3')

    game = Game()

    if game.volume_on:
        pygame.mixer.music.set_volume(1.0)
    else:
        pygame.mixer.music.set_volume(0.0)

    pygame.mixer.music.play(-1)
    game.run()


if __name__ == "__main__":
    main()