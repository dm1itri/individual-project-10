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

    def put(self, player_id):
        with db_session.create_session() as session:
            player = session.query(Player).get(player_id)
            if not player:
                abort(404, message=f"Player {player_id} not found")
            player.current_position = request.form['current_position']
            player.skipping_move = request.form['skipping_move']
            session.commit()
        return jsonify({player_id: 'success'})


class ApiGame(Resource):
    def get(self, game_id):
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)
        if not game:
            abort(404, message=f"Game {game_id} not found")
        return jsonify({game_id: game.to_dict(only=('current_player', ))})

    def put(self, game_id):
        with db_session.create_session() as session:
            game = session.query(Game).get(game_id)
            if not game:
                abort(404, message=f"Game {game_id} not found")
            game.current_player = request.form['current_player']
            session.commit()
        return jsonify({game_id: 'success'})
