import pygame


class BlockGroup(pygame.sprite.Group):
    def __init__(self, block_size, color, starting_pos):
        super().__init__()
        b1 = SingleBlock(color, block_size, block_size * starting_pos[0][0], block_size * starting_pos[0][1])
        b2 = SingleBlock(color, block_size, block_size * starting_pos[1][0], block_size * starting_pos[1][1])
        b3 = SingleBlock(color, block_size, block_size * starting_pos[2][0], block_size * starting_pos[2][1])
        b4 = SingleBlock(color, block_size, block_size * starting_pos[3][0], block_size * starting_pos[3][1])
        self.add(b1, b2, b3, b4)

        self.block_size = block_size

    def rotate(self):
        pass

    def move_to_bottom(self):
        # This one might be generalizable and not have to be overwritten in child classes
        print("moving to bottom")
        pass

    def update(self, *args):
        """ The regular one-block downward tick of the active piece"""
        self.move_blocks(0, self.block_size)

    def move_blocks(self, _dx, _dy):
        legal_move = True
        for block in self.sprites():
            new_block_pos = block.request_move(_dx, _dy)
            if new_block_pos.center[0] > (self.block_size * 11) or \
                    new_block_pos.center[0] < self.block_size or \
                    new_block_pos.center[1] > (self.block_size * 20):
                legal_move = False
        if legal_move:
            for block in self.sprites():
                block.accept_move()


class SingleBlock(pygame.sprite.Sprite):
    def __init__(self, color, width, x, y):
        super().__init__()

        self.color = color
        self.image = pygame.Surface([width, width])
        self.image.fill(color)

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

        self.requested_pos = None
        self.collided = False

    def request_move(self, _dx, _dy):
        self.requested_pos = self.rect.move(_dx, _dy)
        return self.requested_pos

    def accept_move(self):
        self.rect = self.requested_pos

    # def update(self):
    #     if not self.collided:
    #         new_position = self.rect.move(0, 20)
    #         self.rect = new_position
    #         if not self.area.contains(new_position):
    #             self.collided = True

    def anchor(self):
        """ One block hit the bottom or another block. Anchor all the sprites"""
        self.rect.move_ip(0, -20)


class LongBarPiece(BlockGroup):
    def __init__(self, block_size):
        super().__init__(block_size, (255, 0, 0), ((5, 0), (5, 1), (5, 2), (5, 3)))

    def rotate(self):
        print("Rotating!")


class SquarePiece(BlockGroup):
    def __init__(self, block_size):
        super().__init__(block_size, (255, 255, 0), ((5, 0), (6, 0), (5, 1), (6, 1)))


class LeftElPiece(BlockGroup):
    def __init__(self, block_size):
        super().__init__(block_size, (0, 255, 0), ((6, 0), (6, 1), (6, 2), (5, 2)))

    def rotate(self):
        print("Rotating!")


class RightElPiece(BlockGroup):
    def __init__(self, block_size):
        super().__init__(block_size, (0, 0, 255), ((5, 0), (5, 1), (5, 2), (6, 2)))

    def rotate(self):
        print("Rotating!")


class TeePiece(BlockGroup):
    def __init__(self, block_size):
        super().__init__(block_size, (0, 255, 255), ((4, 0), (5, 0), (6, 0), (5, 1)))

    def rotate(self):
        print("Rotating!")
