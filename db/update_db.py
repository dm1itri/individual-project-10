from data import db_session
from data.game import Game
from data.player import Player


db_session.global_init("games.sqlite")


def clear_table():
    with db_session.create_session() as session:
        session.query(Game).delete()
        session.query(Player).delete()
        session.commit()


def add_game():
    with db_session.create_session() as session:
        game = Game(current_player=0)
        session.add(game)
        session.commit()


def add_players(game_id, count_players):
    with db_session.create_session() as session:
        for i in range(count_players):
            player = Player()
            player.current_position = 0
            player.skipping_move = False
            player.number_move = i
            player.game_id = game_id
            session.add(player)
        session.commit()


def clear_game_players(game_id):
    with db_session.create_session() as session:
        game = session.query(Game).get(game_id)
        game.current_player = 0
        players = session.query(Player).where(Player.game_id == game.id).all()
        for player in players:
            player.current_position = 0
            player.skipping_move = False
        session.commit()


clear_table()
add_game()
add_players(1, 2)