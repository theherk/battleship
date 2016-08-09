from battleship.game import Game


if __name__ == '__main__':
    game = Game()

    ship1 = ['j6', 'j7']
    ship2 = ['a1', 'a2', 'a3']
    ship3 = ['b1', 'b2', 'b3']
    ship4 = ['f4', 'e4', 'c4', 'd4']
    ship5 = ['d1', 'e1', 'f1', 'g1', 'h1']

    game.add_ship(ship1)
    game.add_ship(ship2)
    game.add_ship(ship3)
    game.add_ship(ship4)
    game.add_ship(ship5)

    for move in [l for ship in [ship1, ship2, ship3, ship4, ship5] for l in ship]:
        print(game.move(move))
