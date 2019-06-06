import sys, pygame

if __name__ == '__main__':

    pygame.init()

    size = width, height = 700, 240
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    surface = pygame.Surface(size)

    ball = pygame.image.load("beach-ball.png")
    ballrect = ball.get_rect()

    long_bar = pygame.draw.polygon(surface, pygame.Color(255, 0, 0, 0), [(0, 0), (30, 0), (30, 120), (0, 120)])
    # long_bar_rect = long_bar.get_rect()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(surface, long_bar)
        pygame.display.flip()
