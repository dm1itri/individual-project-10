from data import db_session
from data.game import Game
from data.player import Player
from data.history_move import HistoryMove
from data.question import Question

import openpyxl


db_session.global_init("db/games.sqlite")


def clear_table(session):
    session.query(Game).delete()
    session.query(Player).delete()
    session.commit()


def add_game(session, number_of_players):
    game = Game(current_player=0, number_of_players=number_of_players)
    session.add(game)
    session.commit()
    return game


def add_null_history_move(session, game_id):
    null_history_move = HistoryMove(game_id=game_id, number_history=0, number_move=-1, number_steps=0)
    session.add(null_history_move)
    session.commit()


def add_players(session, game, number_of_players):
    for i in range(number_of_players):
        player = Player()
        player.current_position = 0
        player.skipping_move = False
        player.number_move = i
        player.game = game
        session.add(player)
    session.commit()


def clear_game_players(session, game_id):
    game = session.query(Game).get(game_id)
    game.current_player = 0
    players = session.query(Player).filter(Player.game_id == game.id).all()
    for player in players:
        player.current_position = 0
        player.skipping_move = False
        player.is_occupied = False
    session.query(HistoryMove).filter(HistoryMove.game_id == game_id).delete()
    history = HistoryMove()
    history.game_id = game_id
    session.add(history)
    session.commit()


def add_question(session, question_d):
    question = Question()
    question.type_question = question_d['type_question']
    question.question = question_d['question']
    question.answer_correct = question_d['answer_correct']
    question.answer_2 = question_d['answer_2']
    question.answer_3 = question_d['answer_3']
    question.answer_4 = question_d['answer_4']
    session.add(question)
    session.commit()


def read_queastions_xlsx(filename):
    wb = openpyxl.load_workbook(filename)
    # Define variable to read the active sheet:
    # Iterate the loop to read the cell values
    keys_d = ['question', 'answer_correct', 'answer_2', 'answer_3', 'answer_4']
    all_questions = []
    for name in ['Биология', 'История', 'География']:
        sheet = wb[name]
        for i in range(1, 6):
            d = {'type_question': name}
            for j in range(1, 6):
                d[keys_d[j - 1]] = sheet.cell(row=i, column=j).value
            all_questions.append(d)
    with db_session.create_session() as session:
        for question in all_questions:
            add_question(session, question)


#read_queastions_xlsx('C:\\Users\\dimma\\Desktop\\SHCOOL\\Исследовательская\\10 класс\\Вопросы.xlsx')
'''''
with db_session.create_session() as session:
    session.query(Question).delete()
    session.commit()
    clear_table(session)
    add_game(session)
    add_players(session, 1, 2)
    '''''


#with db_session.create_session() as session:
#    n = session.query(HistoryMove).filter(1 == HistoryMove.game_id).order_by(HistoryMove.number_history.desc()).all()

#print(n)