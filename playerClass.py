from vector import Vector2d


class Player:
    def __init__(self, initial_position: 'Vector2d', board_size: 'Vector2d') -> None:
        self.pos: 'Vector2d' = initial_position
        self.board_size: 'Vector2d' = board_size

    def can_move(self, offset: 'Vector2d', obsticals) -> bool:
        """Can move in certain direction."""
        changed_pos = self.pos + offset
        if changed_pos in obsticals: return False
        # out of bounds
        if not (0 < changed_pos.x < self.board_size.x and 0 < changed_pos.y < self.board_size.y): return False
        return True

    @staticmethod
    def can_place(pos, tile_pos) -> bool:
        """Can place a tile down at entered position."""
        if tuple(pos - tile_pos) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            return True
        return False

    def move(self, offset: 'Vector2d') -> None:
        """Moves the player."""
        self.pos += offset

