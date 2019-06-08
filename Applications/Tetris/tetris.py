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
        self.left_wall = WallAndFloor(self.block_size, self.block_size * 20, 0, 0)
        self.right_wall = WallAndFloor(self.block_size, self.block_size * 20, self.block_size * 11, 0)
        self.floor = WallAndFloor(self.block_size * 12, self.block_size, 0, self.block_size * 20)

        self.active_piece = self._get_next_block()
        self.on_deck_piece = self._get_next_block()
        self.anchored_pieces = AnchoredBlocks()

    def _check_lateral_collision(self, _last_lateral_move):
        if pygame.sprite.spritecollide(self.left_wall, self.active_piece, False) or \
                pygame.sprite.spritecollide(self.right_wall, self.active_piece, False) or \
                pygame.sprite.groupcollide(self.active_piece, self.anchored_pieces, False, False, collided=None):
            self.active_piece.move(-_last_lateral_move, 0)

    def _move_piece_down(self):
        self.active_piece.move(0, self.block_size)
        if pygame.sprite.spritecollide(self.floor, self.active_piece, False) or \
                pygame.sprite.groupcollide(self.active_piece, self.anchored_pieces, False, False, collided=None):
            self.active_piece.move(0, -self.block_size)
            self.anchored_pieces.add(self.active_piece.sprites())
            self.active_piece = self.on_deck_piece
            self.on_deck_piece = self._get_next_block()
            return True
        return False

    def _move_to_bottom(self):
        anchored = self._move_piece_down()
        while not anchored:
            anchored = self._move_piece_down()

    def _get_next_block(self):
        if self.block_queue:
            return self.block_types[self.block_queue.pop(0)](self.block_size)
        else:
            return self.block_types[random.randrange(0, 5)](self.block_size)

    def _process_events(self):
        lateral_move_this_frame = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self._move_to_bottom()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.active_piece.move(self.block_size, 0)
                lateral_move_this_frame = self.block_size
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.active_piece.move(-self.block_size, 0)
                lateral_move_this_frame = -self.block_size
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.active_piece.rotate()
        return lateral_move_this_frame

    def mainloop(self):

        clock = pygame.time.Clock()
        self.screen.blit(self.background, (0, 0))
        framecount = 0

        while True:

            lateral_move_this_frame = self._process_events()
            if lateral_move_this_frame:
                self._check_lateral_collision(lateral_move_this_frame)

            if not framecount % 5:
                self._move_piece_down()
            # self.anchored_pieces.update()
            self.active_area.fill((0, 0, 0))
            self.screen.blit(self.active_area, (self.block_size, 0))

            self.active_piece.draw(self.screen)
            self.anchored_pieces.draw(self.screen)
            pygame.display.flip()

            framecount += 1

            # Note the arg to clock.tick() is the number of frames requested/second.
            clock.tick(30)


if __name__ == '__main__':

    game = Tetris()
    game.mainloop()
