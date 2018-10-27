import pygame
from battleship import *


def draw_ship(ship, screen):
    corners = ship.corners()
    front_center = ((corners[1][0] + corners[2][0])/2, (corners[1][1] + corners[2][1])/2)
    if type(ship) is DNABattleship:
        color = (150, 0, 0)
    else:
        color = (0, 150, 60)
    pygame.draw.polygon(screen, color, [corners[0], front_center, corners[3]])


def main():
    #   Setup graphics
    pygame.init()
    font = pygame.font.SysFont("calibri", 14)
    screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Battleships")
    width, height = 800, 800
    running = True
    left, right, up, a, d = [False]*5
    #   Create the ships
    ships = []
    for shipnum in range(20):
        ships.append(DNABattleship((width, height)))
    player_ship = PlayerBattleship((width, height))
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    a = True
                elif event.key == pygame.K_d:
                    d = True
                elif event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_UP:
                    up = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    a = False
                elif event.key == pygame.K_d:
                    d = False
                elif event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_UP:
                    up = False

        # Progressing the program
        for ship in ships:
            ship.update(ships)
        player_ship.update(left, right, up, a, d)

        # Drawing everything
        pygame.draw.rect(screen, (0, 0, 0), screen.get_rect())
        resolution_text = font.render(f"{height}, {width}", 0, (100, 100, 0))
        screen.blit(resolution_text, (10, 10))
        for ship in ships:
            draw_ship(ship, screen)
        draw_ship(player_ship, screen)
        # Updating the window
        pygame.display.flip()


if __name__ == '__main__':
    main()