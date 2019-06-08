import pygame


class WallAndFloor(pygame.sprite.Sprite):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.move_ip(x_pos, y_pos)

    def move(self, _dy):
        self.rect = self.rect.move(0, _dy)


class AnchoredBlocks(pygame.sprite.Group):
    def __init__(self):
        super().__init__()


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

    def move(self, _dx, _dy):
        for block in self.sprites():
            block.move(_dx, _dy)


class SingleBlock(pygame.sprite.Sprite):
    def __init__(self, color, width, x, y):
        super().__init__()

        self.block_size = width
        self.color = color
        self.image = pygame.Surface([width, width])
        self.image.fill(color)

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def move(self, _dx, _dy):
        self.rect = self.rect.move(_dx, _dy)


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
