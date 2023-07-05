from os import name, system
from typing import Any


EMPTY_TILE = '-'
ORTHOGONAL_MOVEMENTS = {
    'd': (0, 1),
    'u': (0, -1),
    'l': (-1, 0),
    'r': (1, 0)
}
FILLED_TILE = 'X'


def main() -> None:
    num_players = verified_input('How many players will be playing?\n>>>', int, 'the_input >= 0')
    num_bots = verified_input('How many bots will be playing too?\n>>>', int,
                              f'the_input >= {max(2 - num_players, 0)}')
    width = verified_input('What should be the width of the board?\n>>>', int, 'the_input >= 2')
    height = verified_input('What should be the height of the board?\n>>>', int,
                            f'the_input >= {max((num_players + num_bots) / width, 2)}')
    game(width, height, num_players, num_bots)


def game(width: int, height: int, num_players: int, num_bots: int) -> None:
    """
    :param width: width of board
    :param height: height of board
    :param num_players: number of players
    :param num_bots: number of bots
    """
    players_playing = list(range(num_players + num_bots))
    player_locs: list[tuple[int, int]] = []  # a dictionary for the location of the players, player: location
    placed_tiles: set[tuple[int, int]] = set()  # a set of all tiles placed by the players
    game_running = True
    while game_running:  # one game
        to_remove = set()
        print(players_playing)
        for i in players_playing:  # one round
            if i < num_players:
                player_turn(i, width, height, player_locs, placed_tiles)
            else:
                bot_turn(i, width, height, player_locs, placed_tiles)
            if player_locs[i] == (-1, -1):
                to_remove.add(i)
            if len(players_playing) - len(to_remove) == 1:
                for player in to_remove:
                    players_playing.remove(player)
                to_remove = set()
                print(f'Player {players_playing[0] + 1} won!')
                game_running = False
                break
        for player in to_remove:
            players_playing.remove(player)


def player_turn(player: int, width: int, height: int, player_locs: list[tuple[int, int]],
                placed_tiles: set[tuple[int, int]]) -> None:
    print_board(width, height, player_locs, placed_tiles)
    if len(player_locs) <= player:  # first turn
        print(f'Where would you, player {player + 1}, like to place your bot? ' +
              '(Your position cannot be the same as any of the other players: ' +
              f'{"; ".join([str((pos[0] + 1, pos[1] + 1)) for pos in player_locs])})')
        while True:
            x_pos = verified_input('\tPlease enter the x position:\n\t>>>', int, f'0 < the_input < {width + 1}')
            y_pos = verified_input('\tPlease enter the y position:\n\t>>>', int, f'0 < the_input < {height + 1}')
            pos = x_pos - 1, y_pos - 1
            if pos not in player_locs:
                player_locs.append(pos)
                break
            print('Sorry, your position was already taken by another player')
        print_board(width, height, player_locs, placed_tiles)
        return
    player_pos = player_locs[player]

    # the player moving:
    possible_moves = set()
    for kvp in ORTHOGONAL_MOVEMENTS.items():
        identifier, ortho_movement = kvp
        adj_pos = change_position(player_pos, ortho_movement)
        if width > adj_pos[0] >= 0 and height > adj_pos[1] >= 0 and \
                adj_pos not in player_locs and adj_pos not in placed_tiles:
            possible_moves.add(identifier)
    if len(possible_moves) == 0:
        placed_tiles.add(player_locs[player])
        player_locs[player] = (-1, -1)
        return

    move_dir = verified_input(f'Where would you like to move your bot, player {player + 1}? ' +
                              f'({"/".join(possible_moves)})\n>>>', str, f'the_input in {possible_moves}')
    player_pos = player_locs[player] = change_position(player_locs[player], ORTHOGONAL_MOVEMENTS[move_dir])
    print_board(width, height, player_locs, placed_tiles)

    # the player placing a tile:
    possible_tile_placements = set()
    for kvp in ORTHOGONAL_MOVEMENTS.items():
        identifier, ortho_movement = kvp
        adj_pos = change_position(player_pos, ortho_movement)
        if width > adj_pos[0] >= 0 and height > adj_pos[1] >= 0 and \
                adj_pos not in player_locs and adj_pos not in placed_tiles:
            possible_tile_placements.add(identifier)
    if len(possible_tile_placements) == 0:
        placed_tiles.add(player_locs[player])
        player_locs[player] = (-1, -1)
        return

    move_dir = verified_input(f"Where would you like to place a tile? ({'/'.join(possible_tile_placements)})\n>>>", str,
                              f'the_input in {possible_tile_placements}')
    placed_tiles.add(change_position(player_locs[player], ORTHOGONAL_MOVEMENTS[move_dir]))
    print_board(width, height, player_locs, placed_tiles)
    return


def bot_turn(bot:int, width: int, height: int, player_locs: list[tuple[int, int]],
             placed_tiles: set[tuple[int, int]]):
    pass


def change_position(pos: tuple[int, int], change: tuple[int, int]):
    return pos[0] + change[0], pos[1] + change[1]


def print_board(width: int, height: int, player_locs: list[tuple[int, int]], placed_tiles: set[tuple[int, int]],
                size: int = 0) -> None:
    """
    Prints the board to the console

    :param size: how large one cell of the board is
    :param width: width of board
    :param height: height of board
    :param player_locs: the locations of the players (x, y)
    :param placed_tiles: locations where tiles were placed (x, y)
    """
    if size < 0 or not isinstance(size, int):
        raise ValueError('The size of a cell must be a natural number or zero')
    board = [
        [
            (
                str(player_locs.index((x, y)) + 1) if ((x, y) in player_locs) else
                (FILLED_TILE if (x, y) in placed_tiles else EMPTY_TILE)
            ) for x in range(width)
        ] for y in range(height)
    ]
    if size == 0:
        print(''.join([''.join(line) + '\n' for line in board]))
    # TODO: create a system for any size of cell
    # start_and_end_lines = f'+{"-" * size}+\n'
    # middle_lines = f'|{" " * size}|\n'
    # size //= 2
    # if size == 0:
    #     size = 1
    # i = size
    # start_cell = start_and_end_lines + middle_lines * size + start_and_end_lines
    # horizontal_cells = start_and_end_lines[1:] + middle_lines[1:] * size + start_and_end_lines[1:]
    # vertical_cells = middle_lines * size + start_and_end_lines
    # diagonal_cells = middle_lines[1:] * size + start_and_end_lines[1:]
    # for i, row in enumerate(board):
    #     for j, cell in enumerate(row):
    #         pass


def clear_terminal() -> None:
    """Clears the terminal"""

    # for windows
    if name == 'nt':
        system('cls')

    # for mac and linux
    else:
        system('clear')


def verified_input(prompt: str, target_type: type, *criterias: str) -> Any:
    """
    Prompts the user and verifies that the response can be turned into the target type and passes the criteria.
    If it does not valid, the user will be prompted again with the prompt

    Note that there can be as many criteria as is needed and that it needs to be a conditional statement in the form of
    a string that will be evaluated.
    """
    while True:
        the_input = input(prompt)
        try:
            the_input = target_type(the_input)
            for criteria in criterias:
                assert eval(criteria)
            return the_input
        except Exception as e:
            print(e)
            print(f'Sorry, "{the_input}" is an invalid input. Please try again.')


if __name__ == '__main__':
    main()
