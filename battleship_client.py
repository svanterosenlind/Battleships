import pygame
from battleship import *


def main():
    #   Initialize graphics and things
    pygame.init()
    sea = (800, 800)
    scr = pygame.display.set_mode(sea)
    running = True
    [up, right, left, a, d] = [False]*5
    cl = pygame.time.Clock()
    #   Initialize things
    b = PlayerBattleship(sea)
    boats = []
    for n in range(10):
        boot = DNABattleship(sea)
        boats.append(DNABattleship(sea))
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

        for ball in balls[::-1]:
            ball.update()
            remove = False
            for boat in boats[::-1]:
                if ball.check_collision(boat):
                    remove = True
                    boats.remove(boat)
                    break
            if ball.distance_left < 0:
                remove = True
            if remove:
                balls.remove(ball)
        balls += b.calculate([up, right, left, a, d])
        b.update()

        for boat in boats:
            balls += boat.calculate(boats + [b])
            boat.update()

        # Draw the sea
        pygame.draw.rect(scr, (0, 0, 0), scr.get_rect())
        draw_boat(b, scr)
        for boat in boats:
            draw_boat(boat, scr)
        for ball in balls:
            draw_ball(ball, scr)
        pygame.display.flip()


def draw_boat(b, screen):
    corn = b.corners()
    p1 = tuple(corn[0].tolist())
    p2 = tuple(((corn[1] + corn[2])/2).tolist())
    p3 = tuple(corn[3].tolist())
    if type(b) == PlayerBattleship:
        color = (200, 50, 40)
    else:
        color = (120, 50, 150)
    pygame.draw.polygon(screen, color, [p1, p2, p3])


def draw_ball(b, screen):
    pygame.draw.circle(screen, (100, 0, 0), tuple(b.pos.astype(int).tolist()), 3)

if __name__ == '__main__':
    main()
