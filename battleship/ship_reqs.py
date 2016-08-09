def allowed_len(ships_req, coords):
    return len(coords) in ships_req


def straight(coords):
    """Validate the ship meets some requirements.

    Requirements:
        only deltas on one axis
        length exists in ships_req
    """
    abscissae = [c[0] for c in coords]
    ordinates = [c[1] for c in coords]
    vertical = abscissae[1:] == abscissae[:-1]
    horizontal = ordinates[1:] == ordinates[:-1]
    return sum([vertical, horizontal]) == 1


def contiguous(coords):
    abscissae = [c[0] for c in coords]
    ordinates = [c[1] for c in coords]
    vertical = abscissae[1:] == abscissae[:-1]
    horizontal = ordinates[1:] == ordinates[:-1]
    if vertical:
        edge = sorted(ordinates)
    elif horizontal:
        edge = sorted(abscissae)
    return edge[-1] - edge[0] == len(edge) - 1


def no_crossing(ships, coords):
    """Validate that a ship doesn't cross another's path."""
    return all([c not in [c for ship in ships for c in ship]
                for c in coords])
