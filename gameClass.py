import playerClass
from vector import Vector2d


class Game:
    tiles: list['Vector2d'] = list()  # there are no tiles in the beginning
    curr_player_num = 0


    def __init__(self, player_locations: tuple['Vector2d'], board_size: 'Vector2d') -> None:
        self.players = [playerClass.Player(pos, board_size) for pos in player_locations]
        self.curr_player = self.players[0]
        self.board_size = board_size
        self.player_pos = list(player_locations)

    def player_turn(self, move_dir: 'Vector2d', tile_pos) -> bool:
        temp = self.player_pos[:]
        temp.remove(self.curr_player.pos)
        if not self.curr_player.can_move(move_dir, self.tiles + temp):
            return False
        pos = self.curr_player.pos + move_dir
        if not self.curr_player.can_place(pos, tile_pos):
            return False
        self.curr_player.move(move_dir)
        self.tiles.append(tile_pos)
        return True

    def move_player(self, move_dir: 'Vector2d') -> None:
        """Moves the current player."""
        temp = self.player_pos[:]
        temp.remove(self.curr_player.pos)
        return self.curr_player.move(move_dir)

    def place_tile(self, tile_pos: 'Vector2d') -> bool:
        """Place a tile, making sure that the tile can be placed."""
        if tile_pos not in self.player_pos and tile_pos not in self.tiles:
            self.tiles.append(tile_pos)
            return True
        return False

    def remove_lost(self) -> None:
        """Removes a player of the game if the current player cannot move."""
        pos = self.curr_player.pos
        offsets = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        for offset in offsets:
            if pos + offset not in self.tiles and pos + offset not in self.player_pos:
                break
        else:
            return
        self.player_pos.remove(self.curr_player.pos)
        self.tiles.append(self.curr_player.pos)
        self.players.remove(self.curr_player)

        self.curr_player = self.players[self.curr_player_num]
