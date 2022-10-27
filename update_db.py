from data import db_session
from data.game import Game
from data.player import Player
from data.history_move import HistoryMove

db_session.global_init("db/games.sqlite")

def clear_table(session):
    session.query(Game).delete()
    session.query(Player).delete()
    session.commit()


def add_game(session):
    game = Game(current_player=0)
    session.add(game)
    session.commit()


def add_players(session, game_id, count_players):
    for i in range(4):
        player = Player()
        player.current_position = 0
        player.skipping_move = False
        player.number_move = i
        player.game_id = 1
        session.add(player)
    session.commit()


def clear_game_players(session, game_id):
    game = session.query(Game).get(game_id)
    game.current_player = 0
    players = session.query(Player).filter(Player.game_id == game.id).all()
    for player in players:
        player.current_position = 0
        player.skipping_move = False
        player.is_occupied = False
    session.query(HistoryMove).filter(HistoryMove.game_id == game_id).delete()
    history = HistoryMove()
    history.game_id = game_id
    session.add(history)
    session.commit()


'''''
with db_session.create_session() as session:
    clear_table(session)
    add_game(session)
    add_players(session, 1, 2)
'''''


#with db_session.create_session() as session:
#    n = session.query(HistoryMove).filter(1 == HistoryMove.game_id).order_by(HistoryMove.number_history.desc()).all()

#print(n)