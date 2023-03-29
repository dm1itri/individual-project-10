from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_restful import Api
from data import db_session
from data.player import Player
from update_db import clear_game_players, add_game, add_players, add_null_history_move
from api.routes import ApiGame, ApiPlayers, ApiHistoryMove, ApiQuestion, ApiPlayersStatics

app = Flask(__name__)
db_session.global_init("db/games.sqlite")
api = Api(app)
api.add_resource(ApiGame, '/api/game')
# api.add_resource(ApiPlayer, '/api/player/<int:player_id>')
api.add_resource(ApiPlayers, '/api/players')
api.add_resource(ApiHistoryMove, '/api/history_game')  # /<int:number_history>
api.add_resource(ApiQuestion, '/api/question')
api.add_resource(ApiPlayersStatics, '/api/players_statics')


@app.get('/game/<int:game_id>')
def game(game_id):
    if not request.cookies.get('number_move') or request.cookies.get('game_id') != str(game_id):
        with db_session.create_session() as session:
            player = session.query(Player).filter_by(is_occupied=False,game_id=game_id).order_by(Player.number_move).first()
            if not player:
                return 'К сожалению, игровая комната заполнена'
            player.is_occupied = True
            session.commit()
            res = make_response(render_template('index.html'))
            res.set_cookie('number_move', str(player.number_move))  # , max_age= 60 * 60
            res.set_cookie('game_id', str(game_id))
        return res
    else:
        return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/create_game', methods=['GET', 'POST'])
def create_game():
    if request.method == 'GET':
        return render_template('create_game.html')
    with db_session.create_session() as session:
        game = add_game(session, int(request.form.get('number_of_players')))
        add_players(session, game, int(request.form.get('number_of_players')))
        add_null_history_move(session, game.id)
        return redirect(url_for('game', game_id=game.id))


# with db_session.create_session() as session:
# clear_game_players(session, 1)


if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
