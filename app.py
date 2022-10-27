from flask import Flask, render_template, request, make_response
from flask_restful import Api
from data import db_session
from data.player import Player
from update_db import clear_game_players
from api.routes import ApiGame, ApiPlayers, ApiHistoryMove


app = Flask(__name__)
db_session.global_init("db/games.sqlite")
api = Api(app)
api.add_resource(ApiGame, '/api/game/<int:game_id>')
# api.add_resource(ApiPlayer, '/api/player/<int:player_id>')
api.add_resource(ApiPlayers, '/api/players/<int:game_id>')
api.add_resource(ApiHistoryMove, '/api/history/<int:game_id>')  # /<int:number_history>


@app.get('/')
def index():
    if not request.cookies.get('player_id'):
        # redirect(url_for('cookie_player_id'))
        print(request.cookies.get('player_id'))
        res = make_response("Обновите страницу для начала игры")
        with db_session.create_session() as session:
            player = session.query(Player).filter(Player.is_occupied == False, Player.game_id == 1).order_by(Player.number_move).first()
            if not player:
                return 'К сожалению, игровая комната заполнена'
            player.is_occupied = True
            session.commit()
            res.set_cookie('player_id', str(player.number_move), max_age=60)  # , max_age= 60 * 60
        return res
    else:
        # print(request.cookies.get('player_id'))
        return render_template('index.html')


with db_session.create_session() as session:
    clear_game_players(session, 1)


if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
