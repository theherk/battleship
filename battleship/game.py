from uuid import uuid1

from battleship import ship_reqs
from battleship.model import DataStore


class GameError(Exception):
    pass


class Game(object):
    ships_req = (5, 4, 3, 3, 2)
    loc_map = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
        'e': 5,
        'f': 6,
        'g': 7,
        'h': 8,
        'i': 9,
        'j': 10}
    coord_map = {v: k for k, v in loc_map.items()}
    # contrived data store
    data_store = DataStore()

    def __init__(self, id_=None):
        if id_ is not None:
            self.id_ = id_
            state = self.load()
            self.moves = state['moves']
            self.ship_positions = state['ship_positions']
            self.ship_status = state['ship_status']
            self.ships_to_init = state['ships_to_init']
        else:
            self.id_ = str(uuid1())
            self.moves = []
            self.ship_positions = []
            self.ship_status = None
            self.ships_to_init = list(self.ships_req[:])

    def load(self):
        """Attempt to load game state from data source."""
        # load previous ship_positions, ship_status, and moves
        state = self.data_store.get_the_stuff(self.id_)
        if state is not None:
            return state
        raise GameError('Game {} failed to load.'.format(id_))

    def save(self):
        """Save the current state."""
        self.data_store.save_the_stuff(
            id_=self.id_,
            moves=self.moves,
            ship_positions=self.ship_positions,
            ship_status=self.ship_status)

    @classmethod
    def loc_to_coord(cls, loc):
        """Convert human readable loc to coord tuple."""
        return (cls.loc_map[loc[0]], int(loc[1:]))

    @classmethod
    def coord_to_loc(cls, coord):
        return ''.join([cls.coord_map[coord[0]], str(coord[1])])

    @property
    def ready_for_move(self):
        return True if self.ship_status is not None else False

    def move(self, loc):
        if not self.ready_for_move:
            raise GameError('Must place all ships first.')
        coord = self.loc_to_coord(loc)
        if coord in self.moves:
            raise GameError('Already tried that move.')
        self.moves.append(coord)
        for ship in self.ship_status:
            if coord in ship:
                ship.remove(coord)
                if not ship:
                    self.ship_status.remove(ship)
                    if not self.ship_status:
                        return 'win'
                    return 'sink'
                return 'hit'
        return 'miss'

    def add_ship(self, position):
        """Add a ship.

        Args:
            position (list): list of locs
        """
        coords = [self.loc_to_coord(p) for p in position]
        if not self.ships_to_init:
            raise GameError('No more ships allowed.')
        if coords in self.ship_positions:
            raise GameError('Ship already added.')
        if not ship_reqs.allowed_len(self.ships_req, coords):
            raise GameError('Ship length not allowed.')
        if not ship_reqs.straight(coords):
            raise GameError('Ship must be straight across or down.')
        if not ship_reqs.contiguous(coords):
            raise GameError('All coordinates must be adjacent.')
        if not ship_reqs.no_crossing(self.ship_positions, coords):
            raise GameError("Don't cross the streams.")
        length = len(coords)
        if length not in self.ships_to_init:
            raise GameError('No more of that ship length.')
        self.ship_positions.append(coords)
        self.ships_to_init.remove(length)
        if not self.ships_to_init:
            self.ship_status = self.ship_positions[:]
