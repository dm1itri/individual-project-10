from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_restful import Api
from data import db_session
from data.player import Player
from data.update_db import add_game, add_players, add_null_history_move
from api.routes import ApiGame, ApiPlayers, ApiHistoryMove, ApiQuestion, ApiPlayersStatics
from data.question import Question


app = Flask(__name__)
db_session.global_init("db/games.sqlite")
api = Api(app)
api.add_resource(ApiGame, '/api/game')
api.add_resource(ApiPlayers, '/api/players')
api.add_resource(ApiHistoryMove, '/api/history_game')
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
        game = add_game(session, int(request.form.get('number_of_players')), int(request.form.get('max_number_of_questions')))
        add_players(session, game, int(request.form.get('number_of_players')))
        add_null_history_move(session, game.id)
        return redirect(url_for('.game', game_id=game.id))


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    question = Question()
    question.type_question = request.form.get('typeQuestion')
    question.question = request.form.get('question')
    question.answer_correct = request.form.get('answerCorrect')
    question.answer_2 = request.form.get('secondAnswer')
    question.answer_3 = request.form.get('thirdAnswer')
    question.answer_4 = request.form.get('fourthAnswer')
    with db_session.create_session() as session:
        session.add(question)
        session.commit()
    return redirect(url_for('.add_question'))


if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
