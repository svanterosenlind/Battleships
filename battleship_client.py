import pygame
from battleship import *


def main():
    #   Initialize graphics and things
    pygame.init()
    scr = pygame.display.set_mode((800, 800))
    running = True
    [up, right, left, a, d] = [False]*5
    cl = pygame.time.Clock()
    #   Initialize things
    b = PlayerBattleship()
    balls = []

    while running:
        cl.tick(30)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up = True
                elif event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_a:
                    a = True
                elif event.key == pygame.K_d:
                    d = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_a:
                    a = False
                elif event.key == pygame.K_d:
                    d = False
        # Process the events
        balls += b.shoot([a, d])
        for ball in balls[::-1]:
            ball.update()
            if ball.distance_left < 0:
                balls.remove(ball)
        b.calculate_FM([up, right, left])
        b.update()

        # Draw the sea
        pygame.draw.rect(scr, (0, 0, 0), scr.get_rect())
        draw_boat(b, scr)
        for ball in balls:
            draw_ball(ball, scr)
        pygame.display.flip()

def draw_boat(b, screen):
    corn = b.corners()
    p1 = tuple(corn[0].tolist())
    p2 = tuple(((corn[1] + corn[2])/2).tolist())
    p3 = tuple(corn[3].tolist())
    pygame.draw.polygon(screen, (200, 50, 40), [p1, p2, p3])


def draw_ball(b, screen):
    pygame.draw.circle(screen, (100, 0, 0), tuple(b.pos.astype(int).tolist()), 5)

if __name__ == '__main__':
    main()
