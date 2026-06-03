"""
Main driver file, handling user inputs and displaying the game
"""

import pygame as pg
from chess import engine

title = "Gofis Chess GUI"

width = height = 512
dimension = 8
sq_size = height // dimension
max_fps = 15
images = {}


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        images[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (sq_size, sq_size))


# Main Driver
def main():
    pg.init()
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption(title)
    clock = pg.time.Clock()
    screen.fill((175, 125, 200))
    gs = engine.GameState()
    load_images()
    running = True
    sq_selected = ()  # keeps track of selected fields as (tuple: (row, col)), none is selected right now
    player_clicks = []  # keeps track of player clicks (two tuples: [(6, 4), (4, 4)])


    # Main Loop
    while running:
        for e in pg.event.get():  # e => event
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()  # (x, y) mouse location
                col = location[0] // sq_size
                row = location[1] // sq_size

                if sq_selected == (col, row):  # if user clicked the same square twice
                    sq_selected = ()  # deselected
                    player_clicks = []  # clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                if len(player_clicks) == 2:  # after 2nd click
                    move = engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move)
                    sq_selected = ()  # reset user clicks
                    player_clicks = []

        draw_gs(screen, gs)
        clock.tick(max_fps)
        pg.display.flip()


# Graphics Driver
def draw_gs(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):  # Board Squares, a8 (top left square) = light
    colors = [pg.Color("white"), pg.Color("gray")]
    for r in range(dimension):            # r => row
        for c in range(dimension):        # c => column
            color = colors[((r+c) % 2)]
            pg.draw.rect(screen, color, pg.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


def draw_pieces(screen, board):  # Board Pieces
    for r in range(dimension):            # r => row
        for c in range(dimension):        # c => column
            piece = board[r][c]

            if piece != "--":  # if field ≠ empty
                screen.blit(images[piece], pg.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


# Run
if __name__ == "__main__":
    main()