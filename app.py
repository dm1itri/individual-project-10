from flask import Flask, jsonify, render_template, redirect, request, make_response, url_for
from flask_restful import Api
from data import db_session
from data.game import Game
from data.player import Player
from api.routes import ApiGame, ApiPlayer, ApiPlayers

app = Flask(__name__)
db_session.global_init("db/games.sqlite")
api = Api(app)
api.add_resource(ApiGame, '/api/game/<int:game_id>')
api.add_resource(ApiPlayer, '/api/player/<int:player_id>')
api.add_resource(ApiPlayers, '/api/players/<int:game_id>')


@app.get('/')
def index():
    if not request.cookies.get('player_id'):
        #redirect(url_for('cookie_player_id'))
        print(request.cookies.get('player_id'))
        res = make_response("Обновите страницу для начала игры")
        with db_session.create_session() as session:
            player = session.query(Player).filter(Player.is_occupied == False, Player.game_id == 1).order_by(Player.number_move).first()
            res.set_cookie('player_id', str(player.number_move), max_age=60)  # , max_age= 60 * 60
            player.is_occupied = True
            session.commit()

        return res
    else:
        print(request.cookies.get('player_id'))
        return render_template('index.html')


@app.get('/cookie_player_id')
def cookie_player_id():
    print(1)
    res = make_response("Setting a cookie")
    with db_session.create_session() as session:
        player = session.query(Player).filter(Player.is_occupied == False, Player.game_id == 1).order_by(Player.number_move).first()
    res.set_cookie('player_id', player.number_move, max_age=60 * 60)  #
    return res


@app.get('/currentPlayer')
def current_player():
    return jsonify({'currentPlayer': 0})


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
        for i in range(4):
            player = Player()
            player.current_position = 0
            player.skipping_move = False
            player.number_move = i
            player.game_id = 1
            session.add(player)
        session.commit()


def clear_game_players(game_id):
    with db_session.create_session() as session:
        game = session.query(Game).get(game_id)
        game.current_player = 0
        players = session.query(Player).filter(Player.game_id == game.id).all()
        for player in players:
            player.current_position = 0
            player.skipping_move = False
            player.is_occupied = False
        session.commit()


clear_game_players(1)
if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
