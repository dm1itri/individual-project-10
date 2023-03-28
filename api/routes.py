from flask_restful import abort, Resource
from flask import jsonify, request
from data import db_session
from data.player import Player
from data.game import Game
from data.history_move import HistoryMove
from data.question import Question
from random import randint


def abort_if_user_not_found(id):
    session = db_session.create_session()
    player = session.get(Player, id)
    if not player:
        abort(404, message=f"User {id} not found")


class ApiPlayers(Resource):
    def get(self):
        game_id = int(request.cookies.get('game_id'))
        with db_session.create_session() as session:
            players = session.query(Player).filter_by(game_id=game_id).order_by(Player.number_move).all()
            number_history = session.query(HistoryMove).filter_by(game_id=game_id).order_by(HistoryMove.number_history.desc()).first().number_history
            response = {
                'current_player': players[0].game.current_player,
                'question_id': players[0].game.question_id,
                'count_players': len(players),
                'number_history': number_history
            }
            for i in range(players[0].game.number_of_players):
                response[f'{i}_player'] = {'current_position': players[i].current_position,
                                           'skipping_move': players[i].skipping_move,
                                           'thinks_about_the_question': players[i].thinks_about_the_question}
        return jsonify(response)


class ApiGame(Resource):
    def get(self):
        game_id = int(request.cookies.get('game_id'))
        with db_session.create_session() as session:
            game = session.get(Game, game_id)
            current_player = session.query(Player).filter_by(game_id=game_id, number_move=game.current_player).first()
            return jsonify(current_player.to_dict(only=('game.current_player', 'game.question_id', 'thinks_about_the_question')))

    def put(self):
        game_id = int(request.cookies.get('game_id'))
        with db_session.create_session() as session:
            player = session.query(Player).filter_by(game_id=game_id, number_move=int(request.form['current_player'])).first()
            player.current_position = int(request.form['current_position'])
            player.skipping_move = int(request.form['skipping_move'])
            player.number_of_points += int(request.form['number_of_points'])
            player.thinks_about_the_question = True if request.form['thinks_about_the_question'] == 'true' else False
            session.commit()
            if not player.thinks_about_the_question:
                curr_player = (int(request.form['current_player']) + 1) % player.game.number_of_players
                for i in range(4):
                    player = session.query(Player).filter(Player.game_id == game_id, Player.number_move == curr_player).first()
                    if player.skipping_move:
                        player.skipping_move = False
                        curr_player = (curr_player + 1) % player.game.number_of_players
                    else:
                        break
                player.game.current_player = curr_player
                player.game.question_id = None
                session.commit()


class ApiHistoryMove(Resource):
    def get(self):
        game_id = int(request.cookies.get('game_id'))
        number_history = request.args.get('number_history', None)

        with db_session.create_session() as session:
            if number_history:
                move = session.query(HistoryMove).filter_by(game_id=game_id, number_history=int(number_history)).first()
            else:
                move = session.query(HistoryMove).filter_by(game_id=game_id).order_by(HistoryMove.number_history.desc()).first()
        if not move:
            return jsonify(None)
        return jsonify(move.to_dict(only=('number_history', 'number_move', 'number_steps')))

    def put(self):
        game_id = int(request.cookies.get('game_id'))
        with db_session.create_session() as session:
            history = HistoryMove()
            history.game_id = game_id
            history.number_history = session.query(HistoryMove).filter_by(game_id=game_id).order_by(HistoryMove.number_history.desc()).first().number_history + 1
            history.number_move = request.form['number_move']
            history.number_steps = request.form['number_steps']
            session.add(history)
            session.commit()


class ApiQuestion(Resource):
    def get(self):
        if request.args.get('question_id') != 'null':
            with db_session.create_session() as session:
                return jsonify(session.get(Question, request.args.get('question_id')).to_dict(only=('question', 'answer_correct', 'answer_2', 'answer_3', 'answer_4')))
        type_question = request.args.get('type_question')
        types_questions_id = {'Биология': (1, 5), 'История': (6, 10), 'География': (11, 15)}
        with db_session.create_session() as session:
            question = session.query(Question).filter_by(type_question=type_question, id=randint(*types_questions_id[type_question])).first()
            game = session.get(Game, int(request.cookies.get('game_id')))
            game.question_id = question.id
            session.commit()
            return jsonify(question.to_dict(only=('question', 'answer_correct', 'answer_2', 'answer_3', 'answer_4')))

