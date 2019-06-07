import sys
from Applications.Tetris.pieces import *


class Tetris(object):
    def __init__(self):
        super().__init__()

        pygame.init()

        self.block_size = 20

        self.board_size = (self.block_size * 12), (self.block_size * 21)  # 240 for the playing width + 420 for height
        self.screen = pygame.display.set_mode(self.board_size)
        self.active_area = pygame.Surface((self.block_size * 10, self.block_size * 20))

        self.background = pygame.image.load("background.png")
        self.background = self.background.convert()

    def mainloop(self):

        # active_piece = LongBarPiece(self.block_size)
        # active_piece = SquarePiece(self.block_size)
        # active_piece = LeftElPiece(self.block_size)
        # active_piece = RightElPiece(self.block_size)
        active_piece = TeePiece(self.block_size)

        clock = pygame.time.Clock()
        self.screen.blit(self.background, (0, 0))

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    active_piece.move_to_bottom()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    active_piece.move_blocks(self.block_size, 0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    active_piece.move_blocks(-self.block_size, 0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    active_piece.rotate()

            active_piece.update()
            # sprites_dict = pygame.sprite.groupcollide(active_piece, group2, dokill1, dokill2, collided=None)
            # if newly_anchored_blocks:
            #     print("Collided!")
            #     newly_anchored_blocks = active_piece.anchor()
                # Also do other stuff like spawn a new active piece, check for full lines, update score, etc etc

            self.active_area.fill((0, 0, 0))
            self.screen.blit(self.active_area, (self.block_size, 0))

            active_piece.draw(self.screen)
            pygame.display.flip()

            # Note the arg to clock.tick() is the number of frames requested/second.
            clock.tick(3)


if __name__ == '__main__':

    game = Tetris()
    game.mainloop()
