from flask_restful import abort, Resource
from flask import jsonify, request
from data import db_session
from data.player import Player
from data.game import Game
from data.history_move import HistoryMove


def abort_if_user_not_found(id):
    session = db_session.create_session()
    player = session.query(Player).get(id)
    if not player:
        abort(404, message=f"User {id} not found")


class ApiPlayers(Resource):
    def get(self, game_id):
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)
            players = session.query(Player).filter(Player.game_id == game.id).order_by(Player.number_move).all()
            number_history = session.query(HistoryMove).filter(game_id == HistoryMove.game_id).order_by(HistoryMove.number_history.desc()).first().number_history
        response = {
            'current_player': game.current_player,
            'count_players': len(players),
            'number_history': number_history
        }
        for i in range(len(players)):
            response[f'{i}_player'] = {'current_position': players[i].current_position,
                                       'skipping_move': players[i].skipping_move}
        print(response)
        return jsonify(response)


class ApiGame(Resource):
    def get(self, game_id):
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)
            # player = session.query(Player).filter(Player.number_move == game.current_player).first()
        return jsonify({game_id: game.to_dict(only=('current_player', ))})

    def put(self, game_id):
        with db_session.create_session() as session:
            players = session.query(Player).filter(Player.game_id == game_id).all()
            count_players = len(players)
            for i in players:
                if i.number_move == int(request.form['current_player']):
                    player = i
            player.current_position = int(request.form['current_position'])
            player.skipping_move = int(request.form['skipping_move'])
            session.commit()

            curr_player = (int(request.form['current_player']) + 1) % count_players
            for i in range(4):
                player = session.query(Player).filter(Player.game_id == game_id, Player.number_move == curr_player).first()
                if player.skipping_move:
                    player.skipping_move = False
                    curr_player = (curr_player + 1) % count_players
                else:
                    break
            game = session.query(Game).get(game_id)
            game.current_player = curr_player
            session.commit()


class ApiHistoryMove(Resource):
    def get(self):
        game_id = int(request.args.get('game_id'))
        number_history = request.args.get('number_history', None)

        with db_session.create_session() as session:
            if number_history:
                move = session.query(HistoryMove).filter(game_id == HistoryMove.game_id, HistoryMove.number_history == int(number_history)).first()
            else:
                move = session.query(HistoryMove).filter(game_id == HistoryMove.game_id).order_by(HistoryMove.number_history.desc()).first()
        if not move:
            return jsonify({game_id: None})
        return jsonify({game_id: move.to_dict(only=('number_history', 'number_move', 'number_steps'))})

    def put(self):
        game_id = int(request.args.get('game_id'))
        with db_session.create_session() as session:
            history = HistoryMove()
            history.game_id = game_id
            history.number_history = session.query(HistoryMove).filter(game_id == HistoryMove.game_id).order_by(HistoryMove.number_history.desc()).first().number_history + 1
            history.number_move = request.form['number_move']
            history.number_steps = request.form['number_steps']
            session.add(history)
            session.commit()

