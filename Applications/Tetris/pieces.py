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
    def __init__(self, block_size, color, starting_pos, rotation_definitions):
        super().__init__()
        self.b0 = SingleBlock(color, block_size, block_size * starting_pos[0][0], block_size * starting_pos[0][1])
        self.b1 = SingleBlock(color, block_size, block_size * starting_pos[1][0], block_size * starting_pos[1][1])
        self.b2 = SingleBlock(color, block_size, block_size * starting_pos[2][0], block_size * starting_pos[2][1])
        self.b3 = SingleBlock(color, block_size, block_size * starting_pos[3][0], block_size * starting_pos[3][1])
        self.add(self.b0, self.b1, self.b2, self.b3)

        self.block_size = block_size
        self.rotations = 0
        self.rotation_definitions = rotation_definitions

    def rotate(self):
        rotation_command = self.rotation_definitions[self.rotations % 4]
        self.b0.move(self.block_size * rotation_command[0][0], self.block_size * rotation_command[0][1])
        self.b1.move(self.block_size * rotation_command[1][0], self.block_size * rotation_command[1][1])
        self.b2.move(self.block_size * rotation_command[2][0], self.block_size * rotation_command[2][1])
        self.b3.move(self.block_size * rotation_command[3][0], self.block_size * rotation_command[3][1])

        self.rotations += 1

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

        rotation_definition = {
            0: [(2, 2), (1, 1), (0, 0), (-1, -1)],
            1: [(-2, -2), (-1, -1), (0, 0), (1, 1)],
            2: [(2, 2), (1, 1), (0, 0), (-1, -1)],
            3: [(-2, -2), (-1, -1), (0, 0), (1, 1)],
        }
        super().__init__(block_size, (255, 0, 0), ((5, 0), (5, 1), (5, 2), (5, 3)), rotation_definition)


class SquarePiece(BlockGroup):
    def __init__(self, block_size):

        rotation_definition = {
            0: [(0, 0), (0, 0), (0, 0), (0, 0)],
            1: [(0, 0), (0, 0), (0, 0), (0, 0)],
            2: [(0, 0), (0, 0), (0, 0), (0, 0)],
            3: [(0, 0), (0, 0), (0, 0), (0, 0)]
        }
        super().__init__(block_size, (255, 255, 0), ((5, 0), (6, 0), (5, 1), (6, 1)), rotation_definition)


class LeftElPiece(BlockGroup):
    def __init__(self, block_size):

        rotation_definition = {
            0: [(1, 1), (0, 0), (-1, -1), (0, -2)],
            1: [(-1, 1), (0, 0), (1, -1), (2, 0)],
            2: [(-1, -1), (0, 0), (1, 1), (0, 2)],
            3: [(1, -1), (0, 0), (-1, 1), (-2, 0)],
        }
        super().__init__(block_size, (0, 255, 0), ((6, 0), (6, 1), (6, 2), (5, 2)), rotation_definition)


class RightElPiece(BlockGroup):
    def __init__(self, block_size):

        rotation_definition = {
            0: [(1, 1), (0, 0), (-1, -1), (-2, 0)],
            1: [(-1, 1), (0, 0), (1, -1), (0, -2)],
            2: [(-1, -1), (0, 0), (1, 1), (2, 0)],
            3: [(1, -1), (0, 0), (-1, 1), (0, 2)],
        }
        super().__init__(block_size, (0, 0, 255), ((5, 0), (5, 1), (5, 2), (6, 2)), rotation_definition)


class TeePiece(BlockGroup):
    def __init__(self, block_size):

        rotation_definition = {
            0: [(1, -1), (0, 0), (-1, 1), (-1, -1)],
            1: [(1, 1), (0, 0), (-1, -1), (1, -1)],
            2: [(-1, 1), (0, 0), (1, -1), (1, 1)],
            3: [(-1, -1), (0, 0), (1, 1), (-1, 1)],
        }
        super().__init__(block_size, (0, 255, 255), ((4, 0), (5, 0), (6, 0), (5, 1)), rotation_definition)
