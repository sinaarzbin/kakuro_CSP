import csp
from csp import Csp
import pygame
from pygame.locals import *


def create_grid(screen, c, cell_width, cell_height):
    board = c.state
    rows = len(board)
    cols = len(board[0])
    canvas_width = cols * cell_width
    canvas_height = rows * cell_height

    screen.fill((255, 255, 255))

    font = pygame.font.Font('font/comic.ttf', 15)
    font1 = pygame.font.Font('font/comic.ttf', 18)

    # a counter label
    counter_text = font.render('assignments: ' + str(csp.counter), True, (0, 0, 0))
    screen.blit(counter_text, (10, canvas_height + 10))

    # filtering and ordering
    f = ''
    if c.filtering == csp.ARC_CONSISTENCY:
        f = 'arc consistency'
    elif c.filtering == csp.FORWARD_CHECKING:
        f = 'forward checking'
    ovar = ''
    if c.variable_ordering == csp.MCV:
        if f != '':
            ovar = ' | MCV'
        else:
            ovar = 'MCV'
    oval = ''
    if c.value_ordering == csp.LCV:
        if ovar != '':
            oval = ' | LCV'
        else:
            oval = 'LCV'
    filtering_text = font.render(f + ovar + oval, True, (0, 0, 0))
    screen.blit(filtering_text, (10, canvas_height + 50))

    for i in range(rows):
        for j in range(cols):
            cell_value = board[i][j]

            x1 = j * cell_width
            y1 = i * cell_height
            x2 = (j + 1) * cell_width
            y2 = (i + 1) * cell_height

            if cell_value == 'X':
                pygame.draw.rect(screen, (124, 124, 125), (x1, y1, cell_width, cell_height))
            elif '\\' in cell_value:
                index = cell_value.find('\\')
                pygame.draw.rect(screen, (124, 124, 125), (x1, y1, cell_width, cell_height))
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)

                if index < len(cell_value) - 1:  # \n
                    text = font.render(cell_value[index + 1:], True, (0, 0, 0))
                    screen.blit(text, ((x1 + x2) / 2 + 5, (y1 + y2) / 2 - 13))
                if index > 0:  # n\
                    text = font.render(cell_value[:index], True, (0, 0, 0))
                    screen.blit(text, ((x1 + x2) / 2 - 13, (y1 + y2) / 2 + 5))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x1, y1, cell_width, cell_height))
                text = font1.render(str(cell_value), True, (0, 0, 0))
                screen.blit(text, ((x1 + x2) / 2 - 2, (y1 + y2) / 2 - 6))

    # Draw grid lines
    for i in range(rows + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, i * cell_height), (canvas_width, i * cell_height), 2)
    for j in range(cols + 1):
        pygame.draw.line(screen, (0, 0, 0), (j * cell_width, 0), (j * cell_width, canvas_height), 2)


def start_graphic(c: Csp, cell_width=50, cell_height=50):
    pygame.init()
    width, height = cell_width * len(c.state[0]) + 2, cell_width * len(c.state) + 80
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        # Update the matrix here
        create_grid(screen, c, cell_width, cell_height)

        pygame.display.flip()
        clock.tick(1000000)