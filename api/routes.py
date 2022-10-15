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
        return jsonify({player_id: player.to_dict(only=('current_position', 'skipping_move'))})


'''
    def put(self, player_id):
        with db_session.create_session() as session:
            player = session.query(Player).get(player_id)
            if not player:
                abort(404, message=f"Player {player_id} not found")
            print(request.form['current_position'])
            print(request.form['skipping_move'])
            player.current_position = request.form['current_position']
            player.skipping_move = request.form['skipping_move']
            session.commit()
        return jsonify({player_id: 'success'})
'''


class ApiPlayers(Resource):
    def get(self, game_id):
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)
            first_player = game.first_player
            second_player = game.second_player
            third_player = game.third_player
            fourth_player = game.fourth_player
        return jsonify({
            'current_player': game.current_player,
            'first_player': {
                'current_position': game.first_player.current_position,
                'skipping_move': game.first_player.skipping_move
            },
            'second_player': {
                'current_position': game.second_player.current_position,
                'skipping_move': game.second_player.skipping_move
            },
            'third_player': {
                'current_position': game.third_player.current_position,
                'skipping_move': game.third_player.skipping_move
            },
            'fourth_player': {
                'current_position': game.fourth_player.current_position,
                'skipping_move': game.fourth_player.skipping_move
            }
        })


class ApiGame(Resource):
    def get(self, game_id):
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)

            if not game:
                abort(404, message=f"Game {game_id} not found")
            for _ in range(4):
                player = session.query(Player).get(game.current_player + 1)  # т.к. id с 1, а current_player с 0
                print(player)
                if player.skipping_move:
                    player.skipping_move = False
                    game.current_player = (game.current_player + 1) % 4
                    session.commit()
                else:
                    break
        return jsonify({game_id: game.to_dict(only=('current_player',))})

    def put(self, game_id):
        print('put')
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)
            player = session.query(Player).get(int(request.form['current_player']))
            if not game:
                abort(404, message=f"Game {game_id} not found")
            game.current_player = int(request.form['current_player']) % 4
            player.current_position = int(request.form['current_position'])
            player.skipping_move = int(request.form['skipping_move'])
            session.commit()
        return jsonify({game_id: 'success'})
