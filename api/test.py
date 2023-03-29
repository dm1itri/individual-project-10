from requests import get, put
from random import randint

id_game = 1
id_player = 1
type_question = 'Биология'
print(get(f'http://127.0.0.1:5000/api/players_statics').json())
#print(get(f'http://127.0.0.1:5000/api/question?type_question={type_question}').json())

#print(get(f'http://127.0.0.1:5000/api/history_game?game_id={id_game}&number_history=1').json())

#print(get(f'http://127.0.0.1:5000/api/players/{id_game}').json())  # получение всех пользователей

#print(get(f'http://127.0.0.1:5000/api/game/{id_game}').json())  # получение игрока, чей сейчас ход

#print(get(f'http://127.0.0.1:5000/api/player/{id_player}').json())  # получение игрока

#print(put(f'http://127.0.0.1:5000/api/game/{id_game}', data={'current_position': 4, 'current_player': 1, 'skipping_move': 0}).json())


#print(get('http://127.0.0.1:5000/api/game/1').json())
#print(put(f'http://127.0.0.1:5000/api/game/{id_game}', data={'current_position': 7, 'current_player': 0, 'skipping_move': 1}).json())

#print(get('http://127.0.0.1:5000/api/game/1').json())
#print(put(f'http://127.0.0.1:5000/api/game/{id_game}', data={'current_position': 6, 'current_player': 1, 'skipping_move': 0}).json())

#print(get('http://127.0.0.1:5000/api/game/1').json())
#print(put(f'http://127.0.0.1:5000/api/game/{id_game}', data={'current_position': 4, 'current_player': 2, 'skipping_move': 0}).json())

#print(get('http://127.0.0.1:5000/api/game/1').json())
#print(put(f'http://127.0.0.1:5000/api/game/{id_game}', data={'current_position': 7, 'current_player': 3, 'skipping_move': 0}).json())

#print(get('http://127.0.0.1:5000/api/game/1').json())