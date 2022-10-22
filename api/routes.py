from flask_restful import abort, Resource
from flask import jsonify, request
from data import db_session
from data.player import Player
from data.game import Game


def abort_if_user_not_found(id):
    session = db_session.create_session()
    player = session.query(Player).get(id)
    if not player:
        abort(404, message=f"User {id} not found")


class ApiPlayer(Resource):
    def get(self, player_id):
        with db_session.create_session() as session:
            player = session.query(Player).get(player_id)
        if not player:
            abort(404, message=f"Player {player_id} not found")
        return jsonify({player_id: player.to_dict(only=('current_position', 'skipping_move', 'number_move'))})


class ApiPlayers(Resource):
    def get(self, game_id):
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)
            players = session.query(Player).filter(Player.game_id == game.id).order_by(Player.number_move).all()
        response = {
            'current_player': game.current_player,
            'count_players': len(players)
        }
        for i in range(len(players)):
            response[f'{i}_player'] = {'current_position': players[i].current_position,
                                       'skipping_move': players[i].skipping_move}
        return jsonify(response)


class ApiGame(Resource):
    def get(self, game_id):
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)
        return jsonify({game_id: game.to_dict(only=('current_player',))})

    def put(self, game_id):
        print('\nput')
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
        return jsonify({game_id: 'success'})
