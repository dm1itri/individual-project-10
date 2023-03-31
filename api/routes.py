from flask_restful import abort, Resource, reqparse
from flask import jsonify, redirect
from data import db_session
from data.player import Player
from data.game import Game
from data.history_move import HistoryMove
from data.question import Question
from random import randint, choice


class MyResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument('game_id', required=True, type=int, location="cookies")
        self.args = self.reqparse.parse_args()
        self.game_id = self.args['game_id']

    def abort_if_game_over(self):
        with db_session.create_session() as session:
            game = session.get(Game, self.game_id)
        if game.is_over:
            return redirect('/')
            #abort(404, message=f'Game {self.game_id} is over')

    def abort_if_user_not_found(self, id):
        session = db_session.create_session()
        player = session.get(Player, id)
        if not player:
            abort(404, message=f"User {id} not found")


class ApiPlayers(MyResource):
    def get(self):
        with db_session.create_session() as session:
            players = session.query(Player).filter_by(game_id=self.game_id).order_by(Player.number_move).all()
            number_history = session.query(HistoryMove).filter_by(game_id=self.game_id).order_by(HistoryMove.number_history.desc()).first().number_history
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


class ApiGame(MyResource):
    def __init__(self):
        super().__init__()
        self.reqparse.add_argument('current_player', type=int, location="form")
        self.reqparse.add_argument('current_position', type=int, location="form")
        self.reqparse.add_argument('skipping_move', type=int, location="form")
        self.reqparse.add_argument('number_of_points', type=int, location="form")
        self.reqparse.add_argument('thinks_about_the_question', type=int, location="form")
        self.args = self.reqparse.parse_args()

    def get(self):
        with db_session.create_session() as session:
            game = session.get(Game, self.game_id)
            current_player = session.query(Player).filter_by(game_id=self.game_id, number_move=game.current_player).first()
            return jsonify(current_player.to_dict(only=('game.current_player', 'game.question_id', 'thinks_about_the_question', 'game.is_over')))

    def put(self):
        with db_session.create_session() as session:
            player = session.query(Player).filter_by(game_id=self.game_id, number_move=self.args['current_player']).first()
            player.current_position = self.args['current_position']
            player.skipping_move = self.args['skipping_move']
            player.number_of_points += self.args['number_of_points']
            player.thinks_about_the_question = bool(self.args['thinks_about_the_question'])
            if self.args['current_position'] not in (9, 21) and bool(self.args['thinks_about_the_question']) == False:
                player.number_of_correct_answers += self.args['number_of_points']
                player.game.number_of_questions_answered += 1
                if player.game.number_of_questions_answered == player.game.max_number_of_questions:
                    player.game.is_over = True
            session.commit()
            if not player.thinks_about_the_question and not player.game.is_over:
                curr_player = (self.args['current_player'] + 1) % player.game.number_of_players
                for i in range(4):
                    player = session.query(Player).filter(Player.game_id == self.game_id, Player.number_move == curr_player).first()
                    if player.skipping_move:
                        player.skipping_move = False
                        curr_player = (curr_player + 1) % player.game.number_of_players
                    else:
                        break
                player.game.current_player = curr_player
                player.game.question_id = None
                session.commit()


class ApiHistoryMove(MyResource):
    def __init__(self):
        super().__init__()
        self.reqparse.add_argument('number_history', type=int, location="args")
        self.reqparse.add_argument('number_move', type=int, location="form")
        self.reqparse.add_argument('number_steps', type=int, location="form")
        self.args = self.reqparse.parse_args()

    def get(self):
        with db_session.create_session() as session:
            if self.args['number_history']:
                move = session.query(HistoryMove).filter_by(game_id=self.game_id, number_history=self.args['number_history']).first()
            else:
                move = session.query(HistoryMove).filter_by(game_id=self.game_id).order_by(HistoryMove.number_history.desc()).first()
        if not move:
            return jsonify(None)
        return jsonify(move.to_dict(only=('number_history', 'number_move', 'number_steps')))

    def put(self):
        with db_session.create_session() as session:
            history = HistoryMove()
            history.game_id = self.game_id
            history.number_history = session.query(HistoryMove).filter_by(game_id=self.game_id).order_by(HistoryMove.number_history.desc()).first().number_history + 1
            history.number_move = self.args['number_move']
            history.number_steps = self.args['number_steps']
            session.add(history)
            session.commit()


class ApiQuestion(MyResource):
    def __init__(self):
        super().__init__()
        self.reqparse.add_argument('question_id', location="args")
        self.reqparse.add_argument('type_question', type=str, location="args")
        self.args = self.reqparse.parse_args()
        self.question_id, self.type_question = self.args['question_id'], self.args['type_question']

    def get(self):
        if self.question_id != 'null':
            with db_session.create_session() as session:
                return jsonify(session.get(Question, self.question_id).to_dict(only=('question', 'answer_correct', 'answer_2', 'answer_3', 'answer_4')))
        type_question = self.type_question
        if type_question == 'Случайный':
            type_question = choice(['Биология', 'История', 'География'])
        with db_session.create_session() as session:
            question = choice(session.query(Question).filter_by(type_question=type_question).all())
            game = session.get(Game, self.game_id)
            game.question_id = question.id
            player = session.query(Player).filter_by(game_id=game.id, number_move=game.current_player).first()
            player.number_of_questions_received += 1
            session.commit()
            return jsonify(question.to_dict(only=('question', 'answer_correct', 'answer_2', 'answer_3', 'answer_4')))


class ApiPlayersStatics(MyResource):
    def get(self):
        players_statics = {}
        with db_session.create_session() as session:
            players = session.query(Player).filter_by(game_id=self.game_id).all()
            for index, player in enumerate(players):
                players_statics[index] = {'numbers_of_moves': len(session.query(HistoryMove).filter_by(game_id=self.game_id, number_move=index).all()),
                                          'percent_of_correct_answers': f'{round(player.number_of_correct_answers / player.number_of_questions_received  * 100 if player.number_of_questions_received else 0)}%',
                                          **player.to_dict(only=('number_of_points', 'number_of_questions_received'))}

        return jsonify(players_statics)
