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
        self.line_scan = pygame.sprite.GroupSingle(WallAndFloor(self.block_size * 10, self.block_size, self.block_size, 0))

        self.active_piece = self._get_next_block()
        self.on_deck_piece = self._get_next_block()
        self.anchored_pieces = AnchoredBlocks()

        self.framecount = 0
        self.removed_lines = 0
        self.score = 0
        self.game_over = False

        self.clock = pygame.time.Clock()
        self.screen.blit(self.background, (0, 0))

    def _anchor_piece(self):
        self.active_piece.move(0, -self.block_size)
        self.anchored_pieces.add(self.active_piece.sprites())
        self.active_piece = self.on_deck_piece
        self.on_deck_piece = self._get_next_block()
        self._scan_for_completed_lines()
        self._calculate_score()
        self._check_game_over()

    def _calculate_score(self):
        self.score += (self.removed_lines ** 2) * 100 + 10  # 10 per anchored block regardless
        self.removed_lines = 0

    def _check_game_over(self):
        if pygame.sprite.groupcollide(self.anchored_pieces, self.line_scan, False, False, collided=None):
            self.game_over = True

    def _check_lateral_collision(self, _last_lateral_move):
        if pygame.sprite.spritecollide(self.left_wall, self.active_piece, False) or \
                pygame.sprite.spritecollide(self.right_wall, self.active_piece, False) or \
                pygame.sprite.groupcollide(self.active_piece, self.anchored_pieces, False, False, collided=None):
            self.active_piece.move(-_last_lateral_move, 0)

    def _get_board_state(self):
        pass

    def _scan_for_completed_lines(self):
        self.line_scan.sprite.move(self.block_size * 20)
        for line_index in range(20):
            collisions = pygame.sprite.groupcollide(self.anchored_pieces, self.line_scan, False, False, collided=None)
            if len(collisions) == 10:
                for sprite in collisions.keys():
                    sprite.kill()
                self.removed_lines += 1
            elif self.removed_lines and collisions:
                for sprite in collisions.keys():
                    sprite.move(0, self.block_size * self.removed_lines)
            self.line_scan.sprite.move(-self.block_size)

    def _move_piece_laterally(self, _direction):
        if _direction == 'right':
            self.active_piece.move(self.block_size, 0)
            self._check_lateral_collision(self.block_size)
        elif _direction == 'left':
            self.active_piece.move(-self.block_size, 0)
            self._check_lateral_collision(-self.block_size)

    def _move_piece_down(self):
        self.active_piece.move(0, self.block_size)
        if pygame.sprite.spritecollide(self.floor, self.active_piece, False) or \
                pygame.sprite.groupcollide(self.active_piece, self.anchored_pieces, False, False, collided=None):
            self._anchor_piece()
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

    def _rotate_piece(self):
        self.active_piece.rotate()
        if pygame.sprite.spritecollide(self.left_wall, self.active_piece, False) or \
                pygame.sprite.spritecollide(self.right_wall, self.active_piece, False) or \
                pygame.sprite.spritecollide(self.floor, self.active_piece, False) or \
                pygame.sprite.groupcollide(self.active_piece, self.anchored_pieces, False, False, collided=None):
            for extra_rotation in range(3):
                self.active_piece.rotate()

    def _process_human_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self._move_to_bottom()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self._move_piece_laterally('right')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self._move_piece_laterally('left')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._rotate_piece()

    def _process_machine_events(self, _input):
        """
        Possible events are:
            1. Rotate
            2. Drop
            3. Nothing. (How do we define nothing? Explicit? Or lack of any other command meeting a threshold? Both?
            4. Left
            5. Right

        :return:
        """
        pass

    def _paint_screen(self):
        # Display Control - Honestly might turn this off when NEAT is running to really make things fly...
        self.active_area.fill((0, 0, 0))
        self.screen.blit(self.active_area, (self.block_size, 0))
        self.active_piece.draw(self.screen)
        self.anchored_pieces.draw(self.screen)
        pygame.display.flip()

    def mainloop(self):
        while not self.game_over:

            self._process_human_events()
            if not self.framecount % 5:
                self._move_piece_down()
            self._paint_screen()

            # Note the arg to clock.tick() is the number of frames requested/second.
            self.clock.tick(30)
            self.framecount += 1

        return self.score

    def do_frame(self, _input):
        """ Externally-controlled version of mainloop"""
        if _input:
            self._process_machine_events(_input)
        if not self.framecount % 4:
            self._move_piece_down()
        self._paint_screen()
        self.framecount += 1
        return self.game_over, self._get_board_state()


if __name__ == '__main__':

    game = Tetris(block_queue=[1] * 20)
    game.mainloop()
