import sys, pygame


class SingleBlock(pygame.sprite.Sprite):
    def __init__(self, color, width):
        super().__init__()
        self.color = color

        self.image = pygame.Surface([width, width])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()


class Tetris(object):
    def __init__(self):
        super().__init__()

        pygame.init()

        self.board_size = 500, 900
        self.screen = pygame.display.set_mode(self.board_size)
        self.surface = pygame.Surface(self.board_size)

        # TODO: Test code below:

        self.block = SingleBlock((255, 9, 9), 40)

        # TODO: End Test Code

    def mainloop(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.surface, self.block)
            pygame.display.flip()


if __name__ == '__main__':

    """
    So what's the breakdown here? 
    I think dividing everything into single blocks makes the most sense. That way any tetris block is just an
    arrangement of 4 blocks that can be individually deleted. But how do you shift them down once they have been
    deleted? 
    
    I think the sprites and groups will solve this for us. We can define a base sprite as a single block, then place
    those into groups for each type of block.
        When that block ends its downward trip, shift the ownership of the sprits to horizontal line groups. We can
        simply iterate through all the line groups, triggering deletions if the group contains more than (8? 10?)
        blocks. This triggers simple delete and shift operations for the affected groups. 
    Bonus: Adding and removing sprites from groups is a very fast operation.
        
    Sprite and Group documentation will be great here.
    """

    game = Tetris()
    game.mainloop()
