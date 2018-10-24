import pygame


def main():
    pygame.init()
    font = pygame.font.SysFont("calibri", 14)
    screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Space Invaders")
    width, height = 800, 800
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size

        # Progressing the program


        # Drawing everything
        pygame.draw.rect(screen, (0, 0, 0), screen.get_rect())
        resolution_text = font.render(f"{height}, {width}", 0, (100, 100, 0))
        screen.blit(resolution_text, (10, 10))

        # Updating the window
        pygame.display.flip()

if __name__ == '__main__':
    main()