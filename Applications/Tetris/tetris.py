import random
import sys
from Applications.Tetris.pieces import *


class Tetris(object):
    def __init__(self, block_queue=None):
        super().__init__()

        pygame.init()

        self.block_size = 20
        self.block_queue = block_queue

        self.board_size = (self.block_size * 12), (self.block_size * 21)  # 240 for the playing width + 420 for height
        self.screen = pygame.display.set_mode(self.board_size)
        self.active_area = pygame.Surface((self.block_size * 10, self.block_size * 20))

        self.background = pygame.image.load("background.png")
        self.background = self.background.convert()

        self.block_types = [LongBarPiece, SquarePiece, LeftElPiece, RightElPiece, TeePiece]

    def _get_next_block(self):
        if self.block_queue:
            return self.block_types[self.block_queue.pop(0)](self.block_size)
        else:
            return self.block_types[random.randrange(0, 5)](self.block_size)

    def mainloop(self):

        active_piece = self._get_next_block()
        on_deck_piece = self._get_next_block()
        anchored_pieces = AnchoredBlocks()

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
            if active_piece.anchored:
                anchored_pieces.add(active_piece.sprites())
                active_piece = on_deck_piece
                on_deck_piece = self._get_next_block()

            anchored_pieces.update()

            # sprites_dict = pygame.sprite.groupcollide(active_piece, group2, dokill1, dokill2, collided=None)
            # if newly_anchored_blocks:
            #     print("Collided!")
            #     newly_anchored_blocks = active_piece.anchor()
                # Also do other stuff like spawn a new active piece, check for full lines, update score, etc etc

            self.active_area.fill((0, 0, 0))
            self.screen.blit(self.active_area, (self.block_size, 0))

            active_piece.draw(self.screen)
            anchored_pieces.draw(self.screen)
            pygame.display.flip()

            # Note the arg to clock.tick() is the number of frames requested/second.
            clock.tick(3)


if __name__ == '__main__':

    game = Tetris([0, 1, 2, 3, 4])
    game.mainloop()
